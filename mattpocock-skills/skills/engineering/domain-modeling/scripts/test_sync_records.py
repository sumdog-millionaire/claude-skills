"""End-to-end check of the sync_records.py hooks against a throwaway remote. Run: python test_sync_records.py"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).with_name("sync_records.py")
HEADER = '"id","status","layer","area","sub_area","project_taxonomy","priority","risk","built_prototype","built_production","decided","statement","why","alternatives","tracker_issue","settled_by","supersedes","superseded_by","adrs"\n'
ADR = "---\nstatus: accepted\ndate: 2026-10-17\narea: structure\nsub_area: technology\n---\n\n# x\n"


def register(*rows: str) -> str:
    """A valid register; each row is 'D2 ben' (id and statement), and a status of BAD makes it fail the check."""
    lines = []
    for row in rows:
        number, statement = row.split(" ", 1) if " " in row else (row, "seed")
        status = "BAD" if statement == "BAD" else "accepted"
        cells = [number, status, "system", "delivery", "testing", "", "should", "low", "no", "no", "2026-10-17", statement, "", "the other way", "", "", "", "", ""]
        lines.append(",".join(f'"{cell}"' for cell in cells) + "\n")
    return HEADER + "".join(lines)


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
    (seed / "docs/adr").mkdir(parents=True)
    config = {"paths": ["docs/ddr", "docs/adr"], "register": "docs/ddr/register.csv", "adrs": "docs/adr"}
    (seed / "docs/agents/records.json").write_text(json.dumps(config))
    (seed / "docs/ddr").mkdir(parents=True)
    (seed / "docs/ddr/register.csv").write_text(register("D1"))
    (seed / "docs/ddr/project_taxonomy.json").write_text("{}")
    run(seed, "git", "add", "-A")
    run(seed, "git", "commit", "-q", "-m", "seed")
    run(seed, "git", "push", "-q", "origin", "main")
    reg = "docs/ddr/register.csv"

    ben, alex = clone(base, remote, "ben"), clone(base, remote, "alex")
    for person in (ben, alex):
        run(person, "git", "checkout", "-q", "-b", "feature")
        result = hook("session", person)
        assert result.returncode == 0 and not result.stdout, result.stdout
    assert (base / "ben-records" / reg).exists()

    result = edit(ben, reg, register("D1", "D2 ben"))
    assert result.returncode == 0 and not result.stderr, result.stderr
    assert on_main(seed, reg) == register("D1", "D2 ben")

    assert hook("before", alex, alex / reg).returncode == 0
    assert (alex / reg).read_text() == register("D1", "D2 ben"), "before brings a stale copy up to date"
    assert edit(alex, reg, register("D1", "D2 ben", "D3 alex")).returncode == 0
    assert edit(alex, "docs/adr/0001-x.md", ADR).returncode == 0, "a new file is pushed"
    assert on_main(seed, "docs/adr/0001-x.md") == ADR

    result = edit(ben, reg, register("D1", "D2 ben", "D3 alex", "D4 BAD"))
    assert result.returncode == 2 and "SKILL.md" in result.stderr and "check failed" in result.stderr, result.stderr
    assert "BAD" not in on_main(seed, reg)
    assert edit(ben, reg, register("D1", "D2 ben", "D3 alex", "D4 ben")).returncode == 0, "the fix goes through"
    assert on_main(seed, reg) == register("D1", "D2 ben", "D3 alex", "D4 ben")

    assert hook("before", alex, alex / reg).returncode == 0
    (alex / reg).write_text(register("D1", "D2 ben", "D3 alex", "D4 ben", "D5 alex"))
    assert edit(ben, reg, register("D1", "D2 ben", "D3 alex", "D4 ben", "D5 ben")).returncode == 0
    result = hook("after", alex, alex / reg)
    assert result.returncode == 2 and "SKILL.md" in result.stderr, "a same-moment clash stops with a message"
    assert hook("before", alex, alex / reg).returncode == 2, "edits wait until the rebase is resolved"

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
