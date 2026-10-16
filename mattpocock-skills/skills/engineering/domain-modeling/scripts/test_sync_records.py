"""End-to-end check of the sync_records.py hooks against a throwaway remote. Run: python test_sync_records.py"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).with_name("sync_records.py")
CHECK = [sys.executable, "-c", "import sys; sys.exit('BAD' in open('register.csv').read())"]


def run(cwd: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True)


def hook(event: str, cwd: Path, file: Path | None = None) -> subprocess.CompletedProcess:
    call = {"cwd": str(cwd), "tool_input": {"file_path": str(file)}} if file else {"cwd": str(cwd)}
    return subprocess.run([sys.executable, str(SCRIPT), event], input=json.dumps(call), capture_output=True, text=True)


def edit(person: Path, rel: str, text: str) -> subprocess.CompletedProcess:
    """What Claude Code does around one Edit: the before hook, the edit, the after hook."""
    before = hook("before", person, person / rel)
    if before.returncode:
        return before
    (person / rel).parent.mkdir(parents=True, exist_ok=True)
    (person / rel).write_text(text)
    return hook("after", person, person / rel)


def clone(base: Path, remote: Path, name: str) -> Path:
    run(base, "git", "clone", "-q", str(remote), name)
    run(base / name, "git", "config", "user.email", f"{name}@example.com")
    run(base / name, "git", "config", "user.name", name)
    return base / name


def on_main(seed: Path, rel: str) -> str:
    run(seed, "git", "pull", "-q")
    return (seed / rel).read_text()


def main() -> None:
    base = Path(tempfile.mkdtemp())
    remote = base / "remote.git"
    run(base, "git", "init", "-q", "--bare", "-b", "main", str(remote))
    seed = clone(base, remote, "seed")
    (seed / "docs/agents").mkdir(parents=True)
    (seed / "docs/agents/records.json").write_text(json.dumps({"paths": ["register.csv", "docs/adr"], "check": CHECK}))
    (seed / "register.csv").write_text("D1\n")
    run(seed, "git", "add", "-A")
    run(seed, "git", "commit", "-q", "-m", "seed")
    run(seed, "git", "push", "-q", "origin", "main")

    ben, alex = clone(base, remote, "ben"), clone(base, remote, "alex")
    for person in (ben, alex):
        run(person, "git", "checkout", "-q", "-b", "feature")
        result = hook("session", person)
        assert result.returncode == 0 and not result.stdout, result.stdout
    assert (base / "ben-records/register.csv").exists()

    result = edit(ben, "register.csv", "D1\nD2 ben\n")
    assert result.returncode == 0 and not result.stderr, result.stderr
    assert on_main(seed, "register.csv") == "D1\nD2 ben\n"

    assert hook("before", alex, alex / "register.csv").returncode == 0
    assert (alex / "register.csv").read_text() == "D1\nD2 ben\n", "before brings a stale copy up to date"
    assert edit(alex, "register.csv", "D1\nD2 ben\nD3 alex\n").returncode == 0
    assert edit(alex, "docs/adr/0001-x.md", "# x\n").returncode == 0, "a new file is pushed"
    assert on_main(seed, "docs/adr/0001-x.md") == "# x\n"

    result = edit(ben, "register.csv", "D1\nD2 ben\nD3 alex\nD4 BAD\n")
    assert result.returncode == 2 and "SKILL.md" in result.stderr and "check failed" in result.stderr, result.stderr
    assert "BAD" not in on_main(seed, "register.csv")
    assert edit(ben, "register.csv", "D1\nD2 ben\nD3 alex\nD4 ben\n").returncode == 0, "the fix goes through"
    assert on_main(seed, "register.csv").endswith("D4 ben\n")

    assert hook("before", alex, alex / "register.csv").returncode == 0
    (alex / "register.csv").write_text(on_main(seed, "register.csv") + "D5 alex\n")
    assert edit(ben, "register.csv", on_main(seed, "register.csv") + "D5 ben\n").returncode == 0
    result = hook("after", alex, alex / "register.csv")
    assert result.returncode == 2 and "SKILL.md" in result.stderr, "a same-moment clash stops with a message"
    assert hook("before", alex, alex / "register.csv").returncode == 2, "edits wait until the rebase is resolved"

    result = hook("before", ben, ben / "README.md")
    assert result.returncode == 0 and not result.stderr and not result.stdout

    other = base / "other"
    run(base, "git", "init", "-q", "other")
    for folder in (other, Path(tempfile.mkdtemp())):
        for event in ("session", "before", "after"):
            result = hook(event, folder, None if event == "session" else folder / "GLOSSARY.md")
            assert result.returncode == 0 and not result.stdout and not result.stderr, "a project that has not opted in is left alone"
    assert not (base / "other-records").exists()
    print("sync_records: all checks passed")


if __name__ == "__main__":
    main()
