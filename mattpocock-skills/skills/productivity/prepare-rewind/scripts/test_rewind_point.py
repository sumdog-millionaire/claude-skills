"""Check the Claude Code reader on a small transcript built in a temporary folder. Run from this folder: python test_rewind_point.py"""

import json
import tempfile
from pathlib import Path

from rewind_point.claude import read_session

USAGE = {"input_tokens": 10, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 90, "output_tokens": 5}


def record(uuid: str, parent: str | None, kind: str, content: object, meta: bool = False) -> dict:
    """One transcript line; an assistant line carries token usage as Claude Code writes it."""
    message: dict = {"content": content}
    if kind == "assistant":
        message["usage"] = USAGE
    line = {"uuid": uuid, "parentUuid": parent, "type": kind, "message": message}
    if meta:
        line["isMeta"] = True
    return line


def text(words: str) -> dict:
    """A text block as an editor extension stores a typed message."""
    return {"type": "text", "text": words}


def test_reads_typed_messages_in_either_shape() -> None:
    """A typed message counts whether stored as a string or as text blocks; tool results and harness notes do not."""
    lines = [
        record("1", None, "user", [text("Plan the invoice export")]),
        record("2", "1", "assistant", [text("Here is the plan.")]),
        record("3", "2", "user", [{"type": "tool_result", "content": "ok"}]),
        record("4", "3", "user", [text("Base directory for this skill")], meta=True),
        record("5", "4", "assistant", [text("Done.")]),
        record("6", "5", "user", "yes, go ahead"),
        record("7", "6", "assistant", [text("Built.")]),
        record("8", "7", "user", [text("This has come up"), {"type": "image", "source": {}}]),
    ]
    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder) / "session.jsonl"
        path.write_text("\n".join(json.dumps(line) for line in lines), encoding="utf-8")
        session = read_session(path)
    assert session.first_message == "Plan the invoice export", session.first_message
    assert [turn.text for turn in session.turns] == ["Plan the invoice export", "yes, go ahead", "This has come up"], session.turns
    assert [turn.context_tokens for turn in session.turns] == [0, 105, 105], session.turns


if __name__ == "__main__":
    test_reads_typed_messages_in_either_shape()
    print("ok")
