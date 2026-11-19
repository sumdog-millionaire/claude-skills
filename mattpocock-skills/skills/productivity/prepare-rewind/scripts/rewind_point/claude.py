import json
import os
import re
from pathlib import Path

from .models import Session, Turn, states_rewind_point


def list_sessions(repo: Path) -> list[Path]:
    """The running conversation's transcript, which Claude Code names in every shell it starts."""
    folder = Path.home() / ".claude" / "projects" / re.sub(r"[^A-Za-z0-9]", "-", str(repo.resolve()))
    session = folder / f"{os.environ['CLAUDE_CODE_SESSION_ID']}.jsonl"
    if not session.is_file():
        raise FileNotFoundError(f"No transcript for this conversation at {session}")
    return [session]


def typed_text(record: dict) -> str | None:
    """The text of a message the user typed, or None for any other record, such as a tool result or harness note."""
    if record.get("type") != "user" or record.get("isMeta"):
        return None
    content = record["message"]["content"]
    if isinstance(content, str):
        return content
    # An editor extension stores a typed message as blocks, where a tool result is a tool_result block
    if any(block["type"] == "tool_result" for block in content):
        return None
    return "\n".join(block["text"] for block in content if block["type"] == "text")


def read_session(session: Path) -> Session:
    """The first message, and the user's messages on the live branch, oldest first."""
    records = [json.loads(line) for line in session.read_text(encoding="utf-8").splitlines()]
    first_message = next((text for text in map(typed_text, records) if text is not None), None)
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
        elif (text := typed_text(record)) is not None:
            turns.append(Turn(text, context_tokens, marker_seen))
            marker_seen = False
    return Session(first_message, turns)
