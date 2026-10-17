"""Claude Code PreToolUse hook that hides holdout tests from the builder, letting only the tester and validator agents reach them.

The plugin's hooks/hooks.json runs it before every Read, Grep, Glob, Bash, Edit and Write.
A call whose path or command names a holdouts folder is blocked with exit code 2, unless it names only seams.md.
ponytail: Bash is matched on the command text, so `sh -c` or a variable gets round it; a guard against accidents, not a sandbox.
"""

import json
import re
import sys

HOLDOUT_AGENTS = {"tester", "validator"}
PATH_FIELDS = ("file_path", "path", "pattern", "command", "notebook_path")
HOLDOUT_PATH = re.compile(r"[/\\]holdouts\b|\bholdouts[/\\]")


def names_hidden_holdout(tool_input: dict) -> bool:
    """True when any path-like field names a holdouts path other than seams.md."""
    for field in PATH_FIELDS:
        # Split commands and paths into words, so each path is judged on its own
        for word in re.split(r"[\s'\"=]+", str(tool_input.get(field, ""))):
            if HOLDOUT_PATH.search(word) and not word.endswith("seams.md"):
                return True
    return False


def main() -> None:
    """Read the hook call from stdin and block it when the builder reaches for a holdout."""
    call = json.load(sys.stdin)
    # Plugin agents arrive as "<plugin>:<name>"
    agent = call.get("agent_type", "").split(":")[-1]
    if agent in HOLDOUT_AGENTS or not names_hidden_holdout(call.get("tool_input", {})):
        return
    print(
        "Holdout tests are hidden from the builder. Build to seams.md in the holdout folder; the validator agent runs the tests.",
        file=sys.stderr,
    )
    sys.exit(2)


if __name__ == "__main__":
    main()
