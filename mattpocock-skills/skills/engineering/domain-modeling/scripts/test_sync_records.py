"""End-to-end check of the sync_records.py hooks against a throwaway remote. Run: python test_sync_records.py"""

import json
import os
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


def hook(event: str, cwd: Path, trace: Path | None = None) -> subprocess.CompletedProcess:
    env = {**os.environ, "GIT_TRACE": str(trace)} if trace else None
    return subprocess.run([sys.executable, str(SCRIPT), event], input=json.dumps({"cwd": str(cwd)}), capture_output=True, text=True, env=env)


def edit(person: Path, rel: str, text: str) -> subprocess.CompletedProcess:
    """A turn with one edit: refresh on prompt submission, then push on Stop."""
    prompt = hook("prompt", person)
    # A failed refresh exits 0 so the prompt goes through, and says so on stdout.
    if prompt.returncode or prompt.stdout:
        return prompt
    (person / rel).parent.mkdir(parents=True, exist_ok=True)
    (person / rel).write_text(text)
    return hook("stop", person)


def clone(base: Path, remote: Path, name: str) -> Path:
    run(base, "git", "clone", "-q", str(remote), name)
    run(base / name, "git", "config", "user.email", f"{name}@example.com")
    run(base / name, "git", "config", "user.name", name)
    return base / name


def on_main(seed: Path, rel: str) -> str:
    run(seed, "git", "pull", "-q")
    return (seed / rel).read_text()


def commit_count(seed: Path) -> int:
    run(seed, "git", "pull", "-q")
    return int(run(seed, "git", "rev-list", "--count", "HEAD").stdout)


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
        result = hook("prompt", person)
        assert result.returncode == 0 and not result.stdout and not result.stderr, result.stderr
    assert (ben / ".git/records-sync" / reg).exists(), "the sync checkout lives inside .git"
    assert not (base / "ben-records").exists(), "nothing appears beside the project"

    result = edit(ben, reg, register("D1", "D2 ben"))
    assert result.returncode == 0 and not result.stderr, result.stderr
    assert on_main(seed, reg) == register("D1", "D2 ben")

    assert hook("prompt", alex).returncode == 0
    assert (alex / reg).read_text() == register("D1", "D2 ben"), "the next turn starts with current records"
    assert edit(alex, reg, register("D1", "D2 ben", "D3 alex")).returncode == 0
    assert edit(alex, "docs/adr/0001-x.md", ADR).returncode == 0, "a new file is pushed"
    assert on_main(seed, "docs/adr/0001-x.md") == ADR

    result = edit(ben, reg, register("D1", "D2 ben", "D3 alex", "D4 BAD"))
    assert result.returncode == 2 and "SKILL.md" in result.stderr and "check failed" in result.stderr, result.stderr
    assert "BAD" not in on_main(seed, reg)
    assert edit(ben, reg, register("D1", "D2 ben", "D3 alex", "D4 ben")).returncode == 0, "the fix goes through"
    assert on_main(seed, reg) == register("D1", "D2 ben", "D3 alex", "D4 ben")

    assert hook("prompt", alex).returncode == 0
    (alex / reg).write_text(register("D1", "D2 ben", "D3 alex", "D4 ben", "D5 alex"))
    assert edit(ben, reg, register("D1", "D2 ben", "D3 alex", "D4 ben", "D5 ben")).returncode == 0
    result = hook("stop", alex)
    assert result.returncode == 2 and "D5" in result.stderr and "SKILL.md" in result.stderr, "a same-moment clash stops and names the id"
    assert hook("prompt", alex).returncode == 0, "nothing is left half-done, so the next turn starts"
    assert (alex / reg).read_text() == register("D1", "D2 ben", "D3 alex", "D4 ben", "D5 alex"), "a clash leaves the working copy intact"

    for event in ("session", "before", "after"):
        result = hook(event, ben)
        assert result.returncode == 2 and "unknown hook event" in result.stderr, "superseded hook events are removed"

    worktree = base / "ben-worktree"
    run(ben, "git", "worktree", "add", "-q", "-b", "second", str(worktree))
    assert hook("prompt", worktree).returncode == 0
    assert (worktree / reg).read_text() == register("D1", "D2 ben", "D3 alex", "D4 ben", "D5 ben"), "a linked worktree is brought up to date"
    assert edit(worktree, reg, register("D1", "D2 ben", "D3 alex", "D4 ben", "D5 ben", "D6 worktree")).returncode == 0
    assert on_main(seed, reg) == register("D1", "D2 ben", "D3 alex", "D4 ben", "D5 ben", "D6 worktree"), "an edit in a linked worktree reaches main"
    assert not (worktree / ".git/records-sync").exists(), "worktrees share the one sync checkout"

    rows = ("D1", "D2 ben", "D3 alex", "D4 ben", "D5 ben", "D6 worktree")
    trace = base / "sync-git-trace.log"
    assert hook("prompt", worktree, trace).returncode == 0
    count = commit_count(seed)
    assert hook("stop", worktree, trace).returncode == 0 and commit_count(seed) == count, "a turn with no record edits pushes nothing"
    assert trace.read_text().count("built-in: git fetch origin main") == 1, "an idle turn fetches only at its start"
    trace.unlink()

    assert hook("prompt", worktree, trace).returncode == 0
    (worktree / reg).write_text(register(*rows, "D7 one"))
    (worktree / reg).write_text(register(*rows, "D7 one", "D8 two"))
    assert commit_count(seed) == count, "edits stay local until the turn ends"
    assert hook("stop", worktree, trace).returncode == 0
    assert on_main(seed, reg) == register(*rows, "D7 one", "D8 two")
    assert commit_count(seed) == count + 1, "a turn's edits go in one commit"
    assert trace.read_text().count("built-in: git fetch origin main") == 1, "a normal turn fetches only at its start"
    assert hook("stop", worktree).returncode == 0 and commit_count(seed) == count + 1, "a repeated Stop creates no duplicate commit"

    interrupted = clone(base, remote, "interrupted")
    assert hook("prompt", interrupted).returncode == 0
    saved = "docs/adr/0002-interrupted.md"
    (interrupted / saved).write_text(ADR)
    concurrent = "docs/adr/0003-concurrent.md"
    assert edit(ben, concurrent, ADR).returncode == 0
    assert hook("prompt", interrupted).returncode == 0
    assert (interrupted / saved).read_text() == ADR, "the next prompt preserves edits from an interrupted turn"
    result = hook("stop", interrupted)
    assert result.returncode == 0, result.stderr
    for rel in (saved, concurrent):
        assert on_main(seed, rel) == ADR, "non-conflicting concurrent records survive the push"
        assert (interrupted / rel).read_text() == ADR, "the merged records are copied back"

    latest = (*rows, "D7 one", "D8 two")
    first = run(seed, "git", "rev-list", "--max-parents=0", "HEAD").stdout.strip()
    old = clone(base, remote, "old")
    run(old, "git", "checkout", "-q", "-b", "old", first)
    (old / reg).write_bytes(register("D1").replace("\n", "\r\n").encode())
    count = commit_count(seed)
    assert hook("stop", old).returncode == 0 and commit_count(seed) == count, "an old copy differing only in line endings is never pushed"
    assert hook("prompt", old).returncode == 0 and (old / reg).read_text() == register(*latest), "the next turn replaces it with main's"

    (old / reg).write_text(register("D1", "D20 old"))
    assert hook("stop", old).returncode == 0
    assert on_main(seed, reg) == register(*latest, "D20 old"), "a new row on an old copy is appended and main's newer rows stay"

    late = clone(base, remote, "late")
    run(late, "git", "checkout", "-q", "-b", "late", first)
    (late / reg).write_text(register("D1", "D21 late"))
    run(late, "git", "commit", "-qam", "a decision made while the hook was off")
    assert hook("prompt", late).returncode == 0 and (late / reg).read_text() == register("D1", "D21 late"), "switching the hook on keeps a committed row main lacks"
    assert hook("stop", late).returncode == 0
    assert on_main(seed, reg) == register(*latest, "D20 old", "D21 late"), "and pushes it"

    assert hook("prompt", old).returncode == 0
    (old / reg).write_text(register(*latest[1:], "D20 changed", "D21 late"))
    assert hook("stop", old).returncode == 0
    assert on_main(seed, reg) == register(*latest, "D20 changed", "D21 late"), "a changed row is applied and a missing row is not deleted"

    assert hook("prompt", old).returncode == 0
    assert edit(ben, reg, register(*latest, "D20 ben", "D21 late")).returncode == 0
    (old / reg).write_text(register(*latest, "D20 old again", "D21 late"))
    result = hook("stop", old)
    assert result.returncode == 2 and "D20" in result.stderr, "a row main changed after you started stops the push and is named"
    assert on_main(seed, reg) == register(*latest, "D20 ben", "D21 late"), "main keeps the other person's change"

    run(ben, "git", "remote", "set-url", "origin", str(base / "missing.git"))
    result = hook("prompt", ben)
    assert result.returncode == 0 and "fetch" in result.stdout and "investigate" in result.stdout, "a failed refresh tells the agent and lets the prompt through"
    run(ben, "git", "remote", "set-url", "origin", str(remote))

    lock = ben / ".git/worktrees/records-sync/index.lock"
    lock.write_text("")
    result = hook("prompt", ben)
    assert result.returncode == 0 and not result.stdout and not lock.exists(), "a lock left by a killed run is cleared"

    disabled = clone(base, remote, "disabled")
    local_config = disabled / "docs/agents/records.json"
    local_config.write_text(json.dumps({**config, "enabled": False}))
    original = (disabled / reg).read_text()
    (disabled / reg).write_text("unsent local records")
    run(disabled, "git", "remote", "set-url", "origin", str(base / "missing.git"))
    disabled_trace = base / "disabled-git-trace.log"
    for event in ("prompt", "stop"):
        result = hook(event, disabled / "docs", disabled_trace)
        assert result.returncode == 0 and not result.stdout and not result.stderr, result.stderr
    assert (disabled / reg).read_text() == "unsent local records", "disabled sync leaves local records untouched"
    assert not (disabled / ".git/records-sync").exists(), "disabled sync creates no worktree"
    assert "git fetch" not in disabled_trace.read_text() and "git push" not in disabled_trace.read_text(), "the local switch prevents network operations"

    local_config.write_text(json.dumps({**config, "enabled": True}))
    (disabled / reg).write_text(original)
    run(disabled, "git", "remote", "set-url", "origin", str(remote))
    assert hook("prompt", disabled).returncode == 0, "enabled true resumes refreshes"
    assert (disabled / ".git/records-sync").exists()
    paused = "docs/adr/0004-paused.md"
    (disabled / paused).write_text(ADR)
    local_config.write_text(json.dumps({**config, "enabled": False}))
    count = commit_count(seed)
    assert hook("stop", disabled).returncode == 0 and commit_count(seed) == count, "disabling mid-turn prevents a push"
    assert (disabled / paused).read_text() == ADR
    local_config.write_text(json.dumps({**config, "enabled": True}))
    assert hook("prompt", disabled).returncode == 0
    assert hook("stop", disabled).returncode == 0
    assert on_main(seed, paused) == ADR, "re-enabling publishes the preserved edits"

    other = base / "other"
    run(base, "git", "init", "-q", "other")
    for folder in (other, Path(tempfile.mkdtemp())):
        for event in ("prompt", "stop"):
            result = hook(event, folder)
            assert result.returncode == 0 and not result.stdout and not result.stderr, "a project that has not opted in is left alone"
    assert not (other / ".git/records-sync").exists()
    hooks = json.loads((SCRIPT.parents[4] / "hooks/hooks.json").read_text())["hooks"]
    sync_hooks = {
        event: [hook for group in groups for hook in group["hooks"] if "sync_records.py" in hook["command"]]
        for event, groups in hooks.items()
    }
    sync_hooks = {event: commands for event, commands in sync_hooks.items() if commands}
    assert set(sync_hooks) == {"UserPromptSubmit", "Stop"}, "records sync runs only at turn boundaries"
    for event, argument in (("UserPromptSubmit", "prompt"), ("Stop", "stop")):
        assert len(sync_hooks[event]) == 1 and sync_hooks[event][0]["command"].endswith(f'" {argument}')
    assert any("guard_holdouts.py" in hook["command"] for group in hooks["PreToolUse"] for hook in group["hooks"]), "holdout protection is unchanged"
    print("sync_records: all checks passed")


if __name__ == "__main__":
    main()
