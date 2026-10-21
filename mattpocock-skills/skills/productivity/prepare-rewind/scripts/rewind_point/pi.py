import json
import re
from pathlib import Path

from .models import Turn, states_rewind_point


def find_session(repo: Path) -> Path:
    """The newest Pi session for this repository, counting forked sessions."""
    folder = Path.home() / ".pi" / "agent" / "sessions" / f"--{re.sub(r'[:/\\\\]', '-', str(repo.resolve()))}--"
    sessions = [*folder.glob("*.jsonl"), *folder.glob("*/forks/*.jsonl")]
    if not sessions:
        raise FileNotFoundError(f"No Pi session for {repo} in {folder}")
    return max(sessions, key=lambda path: path.stat().st_mtime)


def read_turns(session: Path) -> list[Turn]:
    """The user's messages on the live branch, oldest first."""
    records = [json.loads(line) for line in session.read_text(encoding="utf-8").splitlines()]
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
        text = "\n".join(block["text"] for block in message["content"] if block["type"] == "text")
        if message["role"] == "assistant":
            usage = message["usage"]
            context_tokens = usage["input"] + usage["cacheRead"] + usage["cacheWrite"] + usage["output"]
            marker_seen |= states_rewind_point(text)
        elif message["role"] == "user":
            turns.append(Turn(text, context_tokens, marker_seen))
            marker_seen = False
    return turns
