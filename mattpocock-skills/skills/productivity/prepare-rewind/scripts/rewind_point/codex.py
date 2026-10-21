import json
from pathlib import Path

from .models import Session, Turn, states_rewind_point


def list_sessions(repo: Path) -> list[Path]:
    """Every Codex session started in this repository, leaving out sub-agents' sessions."""
    folder = Path.home() / ".codex" / "sessions"
    matches = []
    for path in folder.rglob("rollout-*.jsonl"):
        with path.open(encoding="utf-8") as handle:
            meta = json.loads(handle.readline())["payload"]
        is_subagent = isinstance(meta["source"], dict) and "subagent" in meta["source"]
        if not is_subagent and Path(meta["cwd"]).resolve() == repo.resolve():
            matches.append(path)
    if not matches:
        raise FileNotFoundError(f"No Codex session for {repo} in {folder}")
    return matches


def read_session(session: Path) -> Session:
    """The first message, and the user's messages since the last compaction, oldest first."""
    first_message = None
    turns: list[Turn] = []
    context_tokens = 0
    marker_seen = False
    for line in session.read_text(encoding="utf-8").splitlines():
        record = json.loads(line)
        payload = record.get("payload") or {}
        kind = payload.get("type", "")
        if "rollback" in kind or "rolled_back" in kind:
            raise NotImplementedError(f"{session} holds a {kind} event, which this reader has never been tested on")
        if record["type"] == "compacted":
            turns = []
        elif kind == "token_count" and payload["info"]:
            usage = payload["info"]["last_token_usage"]
            context_tokens = usage["input_tokens"] + usage["output_tokens"]
        elif kind == "message" and payload["role"] == "assistant":
            marker_seen |= any(states_rewind_point(block["text"]) for block in payload["content"])
        elif kind == "item_completed" and payload["item"]["type"] == "UserMessage":
            text = "\n".join(block["text"] for block in payload["item"]["content"] if block["type"] == "text")
            if first_message is None:
                first_message = text
            turns.append(Turn(text, context_tokens, marker_seen))
            marker_seen = False
    return Session(first_message, turns)
