"""Claude Code hooks that keep a project's decision records on main, silently unless something fails.

The plugin's hooks/hooks.json runs these in every project:
    SessionStart              sync_records.py session
    PreToolUse  Edit|Write    sync_records.py before
    PostToolUse Edit|Write    sync_records.py after
A project opts in with docs/agents/records.json on origin/main, naming its record paths, register and ADR folder; other folders are left alone.
Each reads the hook's JSON on stdin. A failure tells the agent what happened and where the recovery steps are.
"""

import filecmp
import json
import shutil
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


def roots(start: Path) -> tuple[Path, Path]:
    """The checkout the hook runs in (the main one or a linked worktree) and the one sync checkout in the shared .git folder."""
    common = Path(git(start, "rev-parse", "--path-format=absolute", "--git-common-dir"))
    root = Path(git(start, "rev-parse", "--show-toplevel"))
    return root, common / "records-sync"


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


def is_record(root: Path, paths: list[str], target: Path) -> bool:
    if not target.resolve().is_relative_to(root.resolve()):
        return False
    rel = target.resolve().relative_to(root.resolve()).as_posix()
    return any(rel == p or rel.startswith(p.rstrip("/") + "/") for p in paths)


def pending(root: Path, sync: Path, paths: list[str]) -> list[Path]:
    """Record files edited in the working copy but not yet on main: they differ from both main and the branch."""
    found = []
    for rel in record_files(root, paths):
        on_main = (sync / rel).is_file() and filecmp.cmp(root / rel, sync / rel, shallow=False)
        on_branch = not git(root, "status", "--porcelain", "--", str(rel))
        if not on_main and not on_branch:
            found.append(rel)
    return found


def copy_back(root: Path, sync: Path, paths: list[str]) -> None:
    for rel in record_files(sync, paths):
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(sync / rel, root / rel)


def ensure_sync(root: Path, sync: Path) -> None:
    git(root, "fetch", "origin", "main")
    if not sync.exists():
        git(root, "worktree", "add", "--detach", str(sync), "origin/main")
    if (Path(git(sync, "rev-parse", "--absolute-git-dir")) / "rebase-merge").exists():
        raise SyncError(f"a push stopped on a conflict and the rebase in {sync} is unfinished.")


def pull(root: Path, sync: Path, paths: list[str]) -> None:
    """Bring the sync checkout and the working copy's records to origin/main, unless an edit awaits its push."""
    ensure_sync(root, sync)
    if pending(root, sync, paths):
        return
    git(sync, "checkout", "--detach", "-f", "origin/main")
    copy_back(root, sync, paths)


def push(root: Path, sync: Path, config: dict) -> None:
    ensure_sync(root, sync)
    files = pending(root, sync, config["paths"])
    if not files:
        return
    for rel in files:
        (sync / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(root / rel, sync / rel)
    check = subprocess.run([sys.executable, str(CHECK), config["register"], config["adrs"]], cwd=sync, capture_output=True, text=True)
    if check.returncode:
        git(sync, "checkout", "-f", "HEAD")
        git(sync, "clean", "-fdq", "--", *config["paths"])
        raise SyncError(f"the records check failed, so nothing was pushed:\n{check.stdout}{check.stderr}".strip())
    git(sync, "add", "-A", "--", *[str(f) for f in files])
    git(sync, "commit", "-m", "Records: " + ", ".join(f.as_posix() for f in files))
    try:
        git(sync, "push", "origin", "HEAD:main")
    except SyncError:
        # Someone pushed first: replay this commit on theirs; a real conflict leaves the rebase for the agent.
        git(sync, "fetch", "origin", "main")
        git(sync, "rebase", "origin/main")
        git(sync, "push", "origin", "HEAD:main")
    git(sync, "fetch", "origin", "main")
    copy_back(root, sync, config["paths"])


def fail(event: str, error: Exception) -> None:
    message = f"Decision-record sync failed ({event}): {error}\nWhat to do: {HELP}, section \"Keep the records on main\"."
    # SessionStart passes stdout to the agent; tool hooks pass stderr on exit 2.
    if event == "session":
        print(message)
        sys.exit(0)
    print(message, file=sys.stderr)
    sys.exit(2)


def main() -> None:
    event = sys.argv[1]
    call = json.load(sys.stdin)
    if not opted_in(Path(call["cwd"])):
        return
    try:
        root, sync = roots(Path(call["cwd"]))
        config = load_config(root)
        if event != "session" and not is_record(root, config["paths"], Path(call["tool_input"]["file_path"])):
            return
        if event in ("session", "before"):
            pull(root, sync, config["paths"])
        elif event == "after":
            push(root, sync, config)
        else:
            raise SyncError(f"unknown hook event {event}: use session, before or after.")
    except SyncError as error:
        fail(event, error)


if __name__ == "__main__":
    main()
