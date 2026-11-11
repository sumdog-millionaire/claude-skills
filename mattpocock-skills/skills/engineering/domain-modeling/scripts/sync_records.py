"""Claude Code hooks that keep a project's decision records on main, silently unless something fails.

The plugin's hooks/hooks.json runs these in every project:
    UserPromptSubmit    sync_records.py prompt
    Stop                sync_records.py stop
A project opts in with docs/agents/records.json on origin/main, naming its record paths, register and ADR folder; other folders are left alone.
Records refresh at the start of each turn and push in one commit at its end. Only your own changes reach main: a new register row is
appended, a changed row or file replaces main's only while main still holds the copy you started from, and nothing is ever deleted.
Each reads the hook's JSON on stdin. A failure tells the agent what happened and where the recovery steps are.
"""

import csv
import io
import json
import subprocess
import sys
from pathlib import Path

CONFIG = "docs/agents/records.json"
HELP = Path(__file__).resolve().parents[1] / "SKILL.md"
CHECK = Path(__file__).with_name("check_records.py")


class SyncError(Exception):
    pass


def git(cwd: Path, *args: str) -> str:
    result = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, encoding="utf-8")
    if result.returncode:
        raise SyncError(f"git {' '.join(args)} failed in {cwd}:\n{result.stderr.strip()}")
    return result.stdout.strip()


def opted_in(cwd: Path) -> bool:
    """True only in a git repository whose origin/main holds the records config."""
    return subprocess.run(["git", "rev-parse", "--verify", "--quiet", f"origin/main:{CONFIG}"], cwd=cwd, capture_output=True).returncode == 0


def roots(start: Path) -> tuple[Path, Path, Path]:
    """The checkout the hook runs in, the one sync checkout in the shared .git folder, and this checkout's copies of what the hook last gave it."""
    common = Path(git(start, "rev-parse", "--path-format=absolute", "--git-common-dir"))
    root = Path(git(start, "rev-parse", "--show-toplevel"))
    base = Path(git(start, "rev-parse", "--absolute-git-dir")) / "records-base"
    return root, common / "records-sync", base


def load_config(root: Path) -> dict:
    return json.loads(git(root, "show", f"origin/main:{CONFIG}"))


def record_files(base: Path, paths: list[str]) -> list[Path]:
    """Every file under the record paths in one checkout, relative to it."""
    found = []
    for p in paths:
        target = base / p
        if target.is_dir():
            found += [f.relative_to(base) for f in target.rglob("*") if f.is_file()]
        elif target.is_file():
            found.append(Path(p))
    return found


def read(path: Path) -> bytes | None:
    """A file's bytes with Windows line endings made plain, or None when there is no such file."""
    return path.read_bytes().replace(b"\r\n", b"\n") if path.is_file() else None


def committed(root: Path, rel: Path) -> bytes | None:
    """The branch's committed copy of a record file, or None when the branch has none."""
    if not git(root, "ls-tree", "--name-only", "HEAD", "--", rel.as_posix()):
        return None
    result = subprocess.run(["git", "show", f"HEAD:{rel.as_posix()}"], cwd=root, capture_output=True)
    if result.returncode:
        raise SyncError(f"git show HEAD:{rel.as_posix()} failed in {root}:\n{result.stderr.decode('utf-8', 'replace').strip()}")
    return result.stdout.replace(b"\r\n", b"\n")


def parse(text: bytes) -> tuple[list[str], dict[str, list[str]]]:
    """The register's header and its rows by id; an id held twice stops the sync."""
    records = [cells for cells in csv.reader(io.StringIO(text.decode("utf-8"))) if cells]
    by_id: dict[str, list[str]] = {}
    for cells in records[1:]:
        if cells[0] in by_id:
            raise SyncError(f"the register holds {cells[0]} twice.")
        by_id[cells[0]] = cells
    return records[0], by_id


def unparse(header: list[str], by_id: dict[str, list[str]]) -> bytes:
    """The register written back the way the format requires: every field quoted, one row per line."""
    out = io.StringIO()
    csv.writer(out, quoting=csv.QUOTE_ALL, lineterminator="\n").writerows([header, *by_id.values()])
    return out.getvalue().encode("utf-8")


def merge_register(local: bytes, head: bytes | None, given: bytes | None, main: bytes | None) -> tuple[bytes | None, list[str]]:
    """Main's register with your new rows appended and your changed rows applied, and the ids main changed under you."""
    if main is None:
        return local, []
    mine = parse(local)[1]
    # The copies you may have started from: the branch's commit and the hook's last refresh.
    started = [parse(copy)[1] for copy in (head, given) if copy is not None]
    header, theirs = parse(main)
    if unparse(header, theirs) != main:
        raise SyncError("the register on main does not quote every field one row per line, so rows cannot be merged into it.")
    merged = dict(theirs)
    clashes = []
    for row_id, cells in mine.items():
        if row_id not in theirs:
            # A new id is always added: adding never loses a decision.
            merged[row_id] = cells
            continue
        before = [rows.get(row_id) for rows in started]
        if cells == theirs[row_id] or cells in before:
            continue
        if theirs[row_id] in before:
            merged[row_id] = cells
        else:
            clashes.append(row_id)
    return unparse(header, merged), clashes


def merge_file(rel: Path, local: bytes, head: bytes | None, given: bytes | None, main: bytes | None) -> tuple[bytes | None, list[str]]:
    """Your copy of a whole record file when you changed it and main still holds the copy you started from."""
    if local in (head, given):
        return main, []
    if main is None or main in (head, given):
        return local, []
    return main, [rel.as_posix()]


def merged(root: Path, sync: Path, base: Path, rel: Path, register: str) -> tuple[bytes | None, list[str]]:
    """What main should hold for one record file once your changes are in, and anything main changed under you."""
    local, main = read(root / rel), read(sync / rel)
    if local is None or local == main:
        return main, []
    head, given = committed(root, rel), read(base / rel)
    if rel.as_posix() == register:
        return merge_register(local, head, given, main)
    return merge_file(rel, local, head, given, main)


def refresh(root: Path, sync: Path, base: Path, config: dict) -> None:
    """Copy main's version of every record file you have not changed into the working copy, and keep it as the copy you were given."""
    for rel in record_files(sync, config["paths"]):
        main = read(sync / rel)
        result, clashes = merged(root, sync, base, rel, config["register"])
        # A file holding changes main lacks waits for the push.
        if clashes or result != main:
            continue
        for target in (root / rel, base / rel):
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((sync / rel).read_bytes())


def ensure_sync(root: Path, sync: Path) -> None:
    if not sync.exists():
        git(root, "worktree", "add", "--detach", str(sync), "origin/main")
    git_dir = Path(git(sync, "rev-parse", "--absolute-git-dir"))
    if (git_dir / "rebase-merge").exists():
        raise SyncError(f"an earlier version of this hook left an unfinished rebase in {sync}.")
    # Only this hook uses the sync checkout and it is force-reset next, so a lock here was left by a killed run.
    (git_dir / "index.lock").unlink(missing_ok=True)


def discard(sync: Path, paths: list[str]) -> None:
    git(sync, "checkout", "-f", "HEAD")
    git(sync, "clean", "-fdq", "--", *paths)


def pull(root: Path, sync: Path, base: Path, config: dict) -> None:
    """Bring the sync checkout to origin/main and refresh every record file that holds no change of yours."""
    ensure_sync(root, sync)
    git(sync, "checkout", "--detach", "-f", "origin/main")
    refresh(root, sync, base, config)


def push(root: Path, sync: Path, base: Path, config: dict) -> None:
    """Merge your record changes into main in one commit; a push refused because main moved is merged again once."""
    ensure_sync(root, sync)
    for attempt in (1, 2):
        changed, clashes = [], []
        files = sorted(set(record_files(root, config["paths"])) | set(record_files(sync, config["paths"])))
        for rel in files:
            result, found = merged(root, sync, base, rel, config["register"])
            clashes += found
            if result is not None and result != read(sync / rel):
                (sync / rel).parent.mkdir(parents=True, exist_ok=True)
                (sync / rel).write_bytes(result)
                changed.append(rel)
        if clashes:
            discard(sync, config["paths"])
            raise SyncError(f"main changed {', '.join(clashes)} after you started from it, so nothing was pushed.")
        # A turn that changed no records needs no commit or push.
        if not changed:
            return
        check = subprocess.run([sys.executable, str(CHECK), config["register"], config["adrs"]], cwd=sync, capture_output=True, text=True)
        if check.returncode:
            discard(sync, config["paths"])
            raise SyncError(f"the records check failed, so nothing was pushed:\n{check.stdout}{check.stderr}".strip())
        git(sync, "add", "-A", "--", *[str(f) for f in changed])
        git(sync, "commit", "-m", "Records: " + ", ".join(f.as_posix() for f in changed))
        try:
            git(sync, "push", "origin", "HEAD:main")
            break
        except SyncError:
            if attempt == 2:
                raise
            # Someone pushed first: start again from their main.
            git(sync, "fetch", "origin", "main")
            git(sync, "checkout", "--detach", "-f", "origin/main")
    refresh(root, sync, base, config)


def fail(event: str, error: Exception) -> None:
    message = f"Decision-record sync failed ({event}): {error}\nWhat to do: {HELP}, section \"Keep the records on main\"."
    print(message, file=sys.stderr)
    sys.exit(2)


def main() -> None:
    event = sys.argv[1]
    call = json.load(sys.stdin)
    if not opted_in(Path(call["cwd"])):
        return
    try:
        root, sync, base = roots(Path(call["cwd"]))
        local_config = root / CONFIG
        if local_config.is_file() and json.loads(local_config.read_text(encoding="utf-8")).get("enabled", True) is False:
            return
        if event == "prompt":
            git(root, "fetch", "origin", "main")
        config = load_config(root)
        if event == "prompt":
            pull(root, sync, base, config)
        elif event == "stop":
            push(root, sync, base, config)
        else:
            raise SyncError(f"unknown hook event {event}: use prompt or stop.")
    except SyncError as error:
        fail(event, error)


if __name__ == "__main__":
    main()
