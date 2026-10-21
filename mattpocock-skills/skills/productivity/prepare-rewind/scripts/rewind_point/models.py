import hashlib
import re
from dataclasses import dataclass

# The line an agent writes to state a rewind point, as implement tells it to.
REWIND_MARKER = "**Rewind point.**"


def states_rewind_point(text: str) -> bool:
    """Whether a line opens with the marker, so a quoted mention of it does not count."""
    return any(line.lstrip().startswith(REWIND_MARKER) for line in text.splitlines())


def stream_name(first_message: str) -> str:
    """A filename-safe name for the session, from the opening words of its first message and a fingerprint of all of it."""
    words = re.findall(r"[a-z0-9]+", re.sub(r"<[^>]+>", " ", first_message).lower())[:5]
    fingerprint = hashlib.sha1(first_message.encode("utf-8")).hexdigest()[:4]
    return "-".join([*words, fingerprint])


@dataclass
class Turn:
    """One message the user sent, with the context the agent held just before it."""

    text: str
    context_tokens: int
    follows_rewind_point: bool


@dataclass
class Session:
    """The session's first message, which no rewind or fork removes, and the turns on its live branch."""

    # None for a session the user never typed into.
    first_message: str | None
    turns: list[Turn]
