from dataclasses import dataclass

# The line an agent writes to state a rewind point, as implement tells it to.
REWIND_MARKER = "**Rewind point.**"


def states_rewind_point(text: str) -> bool:
    """Whether a line opens with the marker, so a quoted mention of it does not count."""
    return any(line.lstrip().startswith(REWIND_MARKER) for line in text.splitlines())


@dataclass
class Turn:
    """One message the user sent, with the context the agent held just before it."""

    text: str
    context_tokens: int
    follows_rewind_point: bool
