import json
import re
from pathlib import Path

from .models import Session, Turn, states_rewind_point


def list_sessions(repo: Path) -> list[Path]:
    """Every Pi session for this repository, counting forked sessions."""
    folder = Path.home() / ".pi" / "agent" / "sessions" / f"--{re.sub(r'[:/\\\\]', '-', str(repo.resolve()))}--"
    sessions = [*folder.glob("*.jsonl"), *folder.glob("*/forks/*.jsonl")]
    if not sessions:
        raise FileNotFoundError(f"No Pi session for {repo} in {folder}")
    return sessions


def message_text(message: dict) -> str:
    """The text blocks of a message, joined."""
    return "\n".join(block["text"] for block in message["content"] if block["type"] == "text")


def read_session(session: Path) -> Session:
    """The first message, and the user's messages on the live branch, oldest first."""
    records = [json.loads(line) for line in session.read_text(encoding="utf-8").splitlines()]
    first_message = next(
        (message_text(r["message"]) for r in records if r["type"] == "message" and r["message"]["role"] == "user"),
        None,
    )
    by_id = {record["id"]: record for record in records if "id" in record}
    # Walking parent links from the newest record skips abandoned branches.
    chain = []
    record_id = [record for record in records if "id" in record][-1]["id"]
    while record_id:
        chain.append(by_id[record_id])
        record_id = by_id[record_id].get("parentId")

    turns = []
    context_tokens = 0
    marker_seen = False
    for record in reversed(chain):
        if record["type"] != "message":
            continue
        message = record["message"]
        if message["role"] == "assistant":
            usage = message["usage"]
            context_tokens = usage["input"] + usage["cacheRead"] + usage["cacheWrite"] + usage["output"]
            marker_seen |= states_rewind_point(message_text(message))
        elif message["role"] == "user":
            turns.append(Turn(message_text(message), context_tokens, marker_seen))
            marker_seen = False
    return Session(first_message, turns)
