"""Fail any quote line in a meeting note whose words are not in the transcript turn at its timestamp.

Usage: python check_quotes.py <note.md>
"""

import re
import sys
from pathlib import Path

QUOTE_LINE = re.compile(r"^> (\d{1,2}:\d{2}(?::\d{2})?) ([^:]+): (.+)$")
TIMESTAMP = re.compile(r"\d{1,2}:\d{2}")


def normalise(text: str) -> str:
    """Lowercase, punctuation to spaces, whitespace collapsed."""
    return " ".join(re.sub(r"[^\w]+", " ", text.lower()).split())


def turns(transcript: str) -> list[str]:
    """Split the transcript into turns, each starting at a line that carries a timestamp."""
    lines = transcript.splitlines()
    starts = [i for i, line in enumerate(lines) if TIMESTAMP.search(line)]
    return ["\n".join(lines[a:b]) for a, b in zip(starts, starts[1:] + [len(lines)])]


def check(note: str) -> list[str]:
    """Return one message per quote line not found in the turn at its timestamp."""
    head, marker, transcript = note.partition("\n## Transcript")
    if not marker:
        raise ValueError("note has no '## Transcript' section")
    all_turns = turns(transcript)
    failures = []
    for line in head.splitlines():
        match = QUOTE_LINE.match(line)
        if not match:
            continue
        timestamp, speaker, words = match.groups()
        at_time = [t for t in all_turns if timestamp in t.splitlines()[0]]
        if not any(normalise(words) in normalise(t) for t in at_time):
            failures.append(f"not in the turn at {timestamp}: {line}")
    return failures


def main() -> None:
    failures = check(Path(sys.argv[1]).read_text(encoding="utf-8"))
    for failure in failures:
        print(failure)
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
