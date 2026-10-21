import argparse
import sys
import traceback
from pathlib import Path

from . import claude, codex, opencode, pi
from .models import Session, stream_name

READERS = {"claude": claude, "codex": codex, "opencode": opencode, "pi": pi}


def squash(text: str) -> str:
    """Text with its whitespace collapsed, so a quote matches however lines were wrapped."""
    return " ".join(text.split())


def main() -> None:
    parser = argparse.ArgumentParser(description="List the user's messages with the context before each.")
    parser.add_argument("--agent", required=True, choices=READERS)
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--quote", required=True, help="A distinctive phrase from one of the user's recent messages")
    parser.add_argument("--limit", type=int, default=200_000)
    args = parser.parse_args()

    reader = READERS[args.agent]
    try:
        matches: list[tuple[object, Session]] = []
        for candidate in reader.list_sessions(args.repo):
            session = reader.read_session(candidate)
            if any(squash(args.quote) in squash(turn.text) for turn in session.turns):
                matches.append((candidate, session))
        if len(matches) != 1:
            raise LookupError(f"{len(matches)} sessions for {args.repo} contain the quote {args.quote!r}; need exactly 1")
        (location, session), = matches
    except Exception:  # noqa: BLE001 (every failure is printed in full and exits 1)
        print(f"REWIND POINT FAILED: the {args.agent} reader broke. Tell the user, quoting the error below.")
        traceback.print_exc(file=sys.stdout)
        sys.exit(1)

    print(f"Session: {location}")
    print(f"Stream: {stream_name(session.first_message)}")
    for number, turn in enumerate(session.turns, 1):
        first_words = squash(turn.text)[:70]
        print(f"{number:>3}  {turn.context_tokens:>8,}  {'R' if turn.follows_rewind_point else ' '}  {first_words}")

    stated = [number for number, turn in enumerate(session.turns, 1) if turn.follows_rewind_point]
    under = [number for number, turn in enumerate(session.turns, 1) if turn.context_tokens < args.limit]
    print(f"Stated rewind point: message {stated[-1]}" if stated else "Stated rewind point: none")
    print(f"Latest under {args.limit:,}: message {under[-1]}" if under else f"No message is under {args.limit:,}")


main()
