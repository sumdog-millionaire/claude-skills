import json
import sqlite3
from pathlib import Path

from .models import Session, Turn, states_rewind_point

DATABASE = Path.home() / ".local" / "share" / "opencode" / "opencode.db"


def list_sessions(repo: Path) -> list[str]:
    """The ids of every top-level opencode session in this repository."""
    with sqlite3.connect(f"file:{DATABASE}?mode=ro", uri=True) as connection:
        rows = connection.execute("select id, directory from session where parent_id is null").fetchall()
    sessions = [session_id for session_id, directory in rows if Path(directory).resolve() == repo.resolve()]
    if not sessions:
        raise FileNotFoundError(f"No opencode session for {repo} in {DATABASE}")
    return sessions


def read_session(session: str) -> Session:
    """The first message, and the user's messages before any undo and since the last compaction, oldest first."""
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

    first_message = None
    turns: list[Turn] = []
    context_tokens = 0
    marker_seen = False
    undone = False
    for message_id, data in messages:
        undone |= message_id == undone_from
        message = json.loads(data)
        message_parts = parts_by_message.get(message_id, [])
        text = "\n".join(part["text"] for part in message_parts if part["type"] == "text" and not part.get("synthetic"))
        if message["role"] == "user" and text and first_message is None:
            first_message = text
        if undone:
            continue
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
    return Session(first_message, turns)
