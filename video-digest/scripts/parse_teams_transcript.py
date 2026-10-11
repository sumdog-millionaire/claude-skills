"""Parse a Teams meeting transcript exported as a Word document into the same
`[MM:SS] text` convention transcribe.py produces, so the rest of the skill's
workflow does not need to know which source a transcript came from.

Teams writes one paragraph per turn - `SpeakerName<spaces><timestamp><text,
no separator>` - with a handful of header paragraphs (title, date, duration)
before the first turn and a "stopped transcription" line after the last. This
needs no Word-specific library: a .docx is a zip of XML, and the transcript
export has no tables, images or styling worth a heavier parser.
"""

import argparse
import re
import zipfile
from pathlib import Path
from xml.sax.saxutils import unescape

TURN = re.compile(r"^(?P<speaker>[A-Za-z][\w .'\-]{0,60}?)\s{2,}(?P<ts>\d{1,2}(?::\d{2}){1,2})(?P<text>.*)$", re.S)


def read_paragraphs(docx: Path) -> list[str]:
    """Return each Word paragraph as one string, in document order."""
    xml = zipfile.ZipFile(docx).read("word/document.xml").decode("utf-8")
    paragraphs = re.findall(r"<w:p\b.*?</w:p>", xml, re.S)
    texts = []
    for paragraph in paragraphs:
        runs = re.findall(r"<w:t[^>]*>(.*?)</w:t>", paragraph, re.S)
        texts.append(unescape("".join(runs), {"&apos;": "'", "&quot;": '"'}))
    return texts


def to_seconds(timestamp: str) -> int:
    """Convert Teams' `M:SS` or `H:MM:SS` timestamp to total seconds."""
    parts = [int(part) for part in timestamp.split(":")]
    while len(parts) < 3:
        parts.insert(0, 0)
    hours, minutes, seconds = parts
    return hours * 3600 + minutes * 60 + seconds


def parse(paragraphs: list[str]) -> tuple[list[str], list[tuple[int, str, str]]]:
    """Split the header lines (before the first turn) from the speaker turns.

    Returns:
        (header lines, turns as (seconds, speaker, text)).
    """
    header: list[str] = []
    turns: list[tuple[int, str, str]] = []
    for text in paragraphs:
        match = TURN.match(text)
        if match:
            turns.append((to_seconds(match["ts"]), match["speaker"].strip(), match["text"].strip()))
        elif not turns:
            header.append(text)
    return header, turns


def format_transcript(turns: list[tuple[int, str, str]]) -> str:
    """Render turns as `[MM:SS] Speaker: text` - transcribe.py's bracket shape,
    with the speaker name kept in front since Teams already did the diarisation
    a real transcription pass would otherwise have to attempt."""
    return "\n".join(
        f"[{seconds // 60:02d}:{seconds % 60:02d}] {speaker}: {text}" for seconds, speaker, text in turns
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Parse a Teams .docx transcript into [MM:SS] Speaker: text.")
    parser.add_argument("transcript", type=Path, help="Path to the Teams-exported .docx transcript.")
    args = parser.parse_args()

    header, turns = parse(read_paragraphs(args.transcript))
    if not turns:
        raise ValueError(
            f"No speaker turns found in {args.transcript} - is this a Teams transcript export? "
            "Open the file and check the layout by eye rather than guessing at a new pattern."
        )

    text = format_transcript(turns)
    out = args.transcript.with_name("transcript.txt")
    out.write_text(text, encoding="utf-8")

    speakers = sorted({speaker for _, speaker, _ in turns})
    print("\n".join(line for line in header if line.strip()))
    print(f"attendees: {', '.join(speakers)}")
    print(f"wrote {out}")
    print("---")
    print(text)


if __name__ == "__main__":
    main()
