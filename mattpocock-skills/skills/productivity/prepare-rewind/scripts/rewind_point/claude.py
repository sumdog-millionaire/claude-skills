import json
import re
from pathlib import Path

from .models import Turn, states_rewind_point


def find_session(repo: Path) -> Path:
    """The newest Claude Code transcript for this repository."""
    folder = Path.home() / ".claude" / "projects" / re.sub(r"[^A-Za-z0-9]", "-", str(repo.resolve()))
    sessions = list(folder.glob("*.jsonl"))
    if not sessions:
        raise FileNotFoundError(f"No Claude Code session for {repo} in {folder}")
    return max(sessions, key=lambda path: path.stat().st_mtime)


def read_turns(session: Path) -> list[Turn]:
    """The user's messages on the live branch, oldest first."""
    records = [json.loads(line) for line in session.read_text(encoding="utf-8").splitlines()]
    by_uuid = {record["uuid"]: record for record in records if "uuid" in record}
    # Walking parent links from the newest record skips abandoned branches and stops at a compaction.
    chain = []
    uuid = [record for record in records if "uuid" in record][-1]["uuid"]
    while uuid:
        chain.append(by_uuid[uuid])
        uuid = by_uuid[uuid]["parentUuid"]

    turns = []
    context_tokens = 0
    marker_seen = False
    for record in reversed(chain):
        message = record.get("message")
        if record["type"] == "assistant":
            usage = message["usage"]
            context_tokens = (
                usage["input_tokens"]
                + usage["cache_creation_input_tokens"]
                + usage["cache_read_input_tokens"]
                + usage["output_tokens"]
            )
            marker_seen |= any(states_rewind_point(block.get("text", "")) for block in message["content"])
        elif record["type"] == "user" and isinstance(message["content"], str) and not record.get("isMeta"):
            turns.append(Turn(message["content"], context_tokens, marker_seen))
            marker_seen = False
    return turns
