import json
import sqlite3
from pathlib import Path

from .models import Turn, states_rewind_point

DATABASE = Path.home() / ".local" / "share" / "opencode" / "opencode.db"


def find_session(repo: Path) -> str:
    """The id of the newest top-level opencode session in this repository."""
    with sqlite3.connect(f"file:{DATABASE}?mode=ro", uri=True) as connection:
        rows = connection.execute(
            "select id, directory from session where parent_id is null order by time_updated desc"
        ).fetchall()
    for session_id, directory in rows:
        if Path(directory).resolve() == repo.resolve():
            return session_id
    raise FileNotFoundError(f"No opencode session for {repo} in {DATABASE}")


def read_turns(session: str) -> list[Turn]:
    """The user's messages before any undo and since the last compaction, oldest first."""
    with sqlite3.connect(f"file:{DATABASE}?mode=ro", uri=True) as connection:
        (revert,) = connection.execute("select revert from session where id = ?", (session,)).fetchone()
        messages = connection.execute(
            "select id, data from message where session_id = ? order by time_created, id", (session,)
        ).fetchall()
        parts = connection.execute("select message_id, data from part where session_id = ? order by id", (session,))
        parts_by_message: dict[str, list[dict]] = {}
        for message_id, data in parts:
            parts_by_message.setdefault(message_id, []).append(json.loads(data))
    undone_from = json.loads(revert)["messageID"] if revert else None

    turns: list[Turn] = []
    context_tokens = 0
    marker_seen = False
    for message_id, data in messages:
        if message_id == undone_from:
            break
        message = json.loads(data)
        message_parts = parts_by_message.get(message_id, [])
        text = "\n".join(part["text"] for part in message_parts if part["type"] == "text" and not part.get("synthetic"))
        if any(part["type"] == "compaction" for part in message_parts):
            turns = []
        elif message["role"] == "assistant":
            tokens = message["tokens"]
            total = tokens["input"] + tokens["cache"]["read"] + tokens["cache"]["write"] + tokens["output"]
            # A compaction summary leaves only itself in context; an aborted reply reports nothing.
            if message.get("summary") is True:
                context_tokens = tokens["output"]
            elif total:
                context_tokens = total
            marker_seen |= states_rewind_point(text)
        elif message["role"] == "user" and text:
            turns.append(Turn(text, context_tokens, marker_seen))
            marker_seen = False
    return turns
