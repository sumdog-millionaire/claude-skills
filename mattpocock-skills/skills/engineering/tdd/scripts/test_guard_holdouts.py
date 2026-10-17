"""Tests for guard_holdouts.py, fed the JSON a PreToolUse hook receives. Run: pytest test_guard_holdouts.py"""

import json
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).with_name("guard_holdouts.py")
HOLDOUT = "C:/repo/.git/holdouts/ENG-134"


def guard(tool_input: dict, agent_type: str | None = None) -> subprocess.CompletedProcess:
    """Run the hook on one tool call, from the main session or the named agent."""
    call = {"tool_name": "Read", "tool_input": tool_input}
    if agent_type:
        call["agent_type"] = agent_type
    return subprocess.run([sys.executable, str(SCRIPT)], input=json.dumps(call), capture_output=True, text=True)


# === The builder is kept out ===


@pytest.mark.parametrize(
    "tool_input",
    [
        {"file_path": f"{HOLDOUT}/test_basket.py"},
        {"file_path": "C:\\repo\\.git\\holdouts\\ENG-134\\test_basket.py"},
        {"path": ".git/holdouts", "pattern": "total"},
        {"pattern": "**/holdouts/**"},
        {"command": f"cat {HOLDOUT}/test_basket.py"},
        {"command": "ls .git/holdouts"},
        {"command": "pytest tests/holdouts/test_basket.py"},
    ],
)
def test_builder_is_blocked_from_holdouts(tool_input: dict) -> None:
    result = guard(tool_input)
    assert result.returncode == 2
    assert "seams.md" in result.stderr


def test_builder_is_blocked_from_writing_holdouts() -> None:
    assert guard({"file_path": f"{HOLDOUT}/test_basket.py", "content": "x"}).returncode == 2


# === What the builder may still do ===


@pytest.mark.parametrize(
    "tool_input",
    [
        {"file_path": f"{HOLDOUT}/seams.md"},
        {"command": f'cat "{HOLDOUT}/seams.md"'},
        {"file_path": "src/basket.py"},
        {"command": "grep -r holdouts docs"},
        {"command": 'git commit -m "Explain holdouts in the readme"'},
        {"file_path": "docs/notes.md", "old_string": "/holdouts/x", "new_string": "y"},
    ],
)
def test_builder_keeps_seams_and_everything_else(tool_input: dict) -> None:
    assert guard(tool_input).returncode == 0


# === The tester and validator are let through ===


@pytest.mark.parametrize("agent_type", ["mattpocock-skills:tester", "mattpocock-skills:validator", "tester", "validator"])
def test_tester_and_validator_reach_holdouts(agent_type: str) -> None:
    assert guard({"file_path": f"{HOLDOUT}/test_basket.py"}, agent_type).returncode == 0


def test_other_subagents_are_blocked() -> None:
    assert guard({"file_path": f"{HOLDOUT}/test_basket.py"}, "Explore").returncode == 2
