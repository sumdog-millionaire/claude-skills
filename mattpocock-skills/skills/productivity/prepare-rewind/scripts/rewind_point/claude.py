import json
import re
from pathlib import Path

from .models import Session, Turn, states_rewind_point


def list_sessions(repo: Path) -> list[Path]:
    """Every Claude Code transcript for this repository."""
    folder = Path.home() / ".claude" / "projects" / re.sub(r"[^A-Za-z0-9]", "-", str(repo.resolve()))
    sessions = list(folder.glob("*.jsonl"))
    if not sessions:
        raise FileNotFoundError(f"No Claude Code session for {repo} in {folder}")
    return sessions


def is_user_text(record: dict) -> bool:
    """Whether a record is a message the user typed, not a tool result or harness note."""
    return record.get("type") == "user" and isinstance(record["message"]["content"], str) and not record.get("isMeta")


def read_session(session: Path) -> Session:
    """The first message, and the user's messages on the live branch, oldest first."""
    records = [json.loads(line) for line in session.read_text(encoding="utf-8").splitlines()]
    first_message = next((record["message"]["content"] for record in records if is_user_text(record)), None)
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
        if record["type"] == "assistant":
            usage = record["message"]["usage"]
            context_tokens = (
                usage["input_tokens"]
                + usage["cache_creation_input_tokens"]
                + usage["cache_read_input_tokens"]
                + usage["output_tokens"]
            )
            marker_seen |= any(states_rewind_point(block.get("text", "")) for block in record["message"]["content"])
        elif is_user_text(record):
            turns.append(Turn(record["message"]["content"], context_tokens, marker_seen))
            marker_seen = False
    return Session(first_message, turns)
