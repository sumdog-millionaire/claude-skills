"""Self-check for check_quotes.py. Run: python test_check_quotes.py"""

from check_quotes import check

TRANSCRIPT = """
## Transcript

**Sam Okafor** 12:03 Refunds always go back to the card they paid with,
no store credit.

**Lee Chen** 12:20 Agreed, card only.
"""

UNTIMED = """
## Transcript

Refunds always go back to the card they paid with.

Agreed, card only.
"""


def test() -> None:
    assert check("> 12:03 Sam Okafor: refunds always go back to the card" + TRANSCRIPT) == []
    assert check("> 12:03 Sam Okafor: paid with, no store credit" + TRANSCRIPT) == []
    assert len(check("> 12:03 Sam Okafor: refunds go to store credit" + TRANSCRIPT)) == 1
    assert len(check("> 12:09 Sam Okafor: no store credit" + TRANSCRIPT)) == 1
    assert len(check("> 12:20 Lee Chen: no store credit" + TRANSCRIPT)) == 1
    assert check("> Sam Okafor: back to the card they paid with" + UNTIMED) == []
    assert len(check("> Sam Okafor: refunds go to store credit" + UNTIMED)) == 1
    try:
        check("> 12:03 Sam Okafor: no store credit")
    except ValueError:
        pass
    else:
        raise AssertionError("a note without a transcript must raise")
    print("ok")


if __name__ == "__main__":
    test()
