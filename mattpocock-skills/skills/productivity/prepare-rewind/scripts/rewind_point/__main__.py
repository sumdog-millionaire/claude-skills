import argparse
import sys
import traceback
from pathlib import Path

from . import claude, codex, opencode, pi

READERS = {"claude": claude, "codex": codex, "opencode": opencode, "pi": pi}


def main() -> None:
    parser = argparse.ArgumentParser(description="List the user's messages with the context before each.")
    parser.add_argument("--agent", required=True, choices=READERS)
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--limit", type=int, default=200_000)
    args = parser.parse_args()

    reader = READERS[args.agent]
    try:
        session = reader.find_session(args.repo)
        turns = reader.read_turns(session)
        if not turns:
            raise ValueError(f"{session} has no user messages on its live branch")
    except Exception:  # noqa: BLE001 (every failure is printed in full and exits 1)
        print(f"REWIND POINT FAILED: the {args.agent} reader broke. Tell the user, quoting the error below.")
        traceback.print_exc(file=sys.stdout)
        sys.exit(1)

    print(f"Session: {session}")
    for number, turn in enumerate(turns, 1):
        first_words = " ".join(turn.text.split())[:70]
        print(f"{number:>3}  {turn.context_tokens:>8,}  {'R' if turn.follows_rewind_point else ' '}  {first_words}")

    stated = [number for number, turn in enumerate(turns, 1) if turn.follows_rewind_point]
    under = [number for number, turn in enumerate(turns, 1) if turn.context_tokens < args.limit]
    print(f"Stated rewind point: message {stated[-1]}" if stated else "Stated rewind point: none")
    print(f"Latest under {args.limit:,}: message {under[-1]}" if under else f"No message is under {args.limit:,}")


main()
