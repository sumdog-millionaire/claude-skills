# /// script
# dependencies = [
#     "faster-whisper==1.2.1",
#     # av 18 ships DLLs that Windows Application Control policies block on some
#     # machines, so the pin stays at 17.0.1 until both are re-tested together.
#     "av==17.0.1",
# ]
# ///
"""Transcribe a video to timestamped text using faster-whisper (ASR only, no diarisation)."""

import argparse
import time
from pathlib import Path

from faster_whisper import WhisperModel

# English distil model: ~3x faster than realtime on CPU, weights already cached
# locally. Speaker diarisation is deliberately absent - a reel is one talking
# head, and diarisation costs more time than the whole transcription.
MODEL = "distil-large-v3"


def transcribe(video: Path, language: str = "en") -> tuple[list[tuple[float, str]], float, float]:
    """Transcribe video into timestamped lines.

    Args:
        video: any ffmpeg-decodable media file.
        language: ISO code passed to Whisper; forcing it avoids a detection pass.

    Returns:
        (lines as (start seconds, text), audio duration in seconds, wall time in seconds).
    """
    started = time.perf_counter()
    model = WhisperModel(MODEL, device="cpu", compute_type="int8")
    # vad_filter drops silence and background music, which keeps Whisper from
    # hallucinating lyrics into the gaps between spoken lines.
    segments, info = model.transcribe(str(video), language=language, vad_filter=True)
    lines = [(segment.start, segment.text.strip()) for segment in segments]
    return lines, info.duration, time.perf_counter() - started


def format_transcript(lines: list[tuple[float, str]]) -> str:
    """Render lines as `[MM:SS] text`, so a spoken moment maps onto a frame file."""
    return "\n".join(
        f"[{int(start) // 60:02d}:{int(start) % 60:02d}] {text}" for start, text in lines
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Transcribe a video to timestamped text.")
    parser.add_argument("video", type=Path, help="Path to the downloaded video file.")
    parser.add_argument("--language", default="en", help="Spoken language (default: en).")
    args = parser.parse_args()

    lines, duration, elapsed = transcribe(args.video, args.language)
    text = format_transcript(lines)
    transcript = args.video.with_name("transcript.txt")
    transcript.write_text(text, encoding="utf-8")

    words = sum(len(line.split()) for _, line in lines)
    # Words per minute is what tells the caller whether this is real speech: a
    # talking head runs 120-200, a music-only clip lands near zero.
    wpm = words / (duration / 60) if duration else 0
    print(f"audio {duration:.1f}s | wall {elapsed:.1f}s | {words} words | {wpm:.0f} wpm")
    print(f"wrote {transcript}")
    print("---")
    print(text)


if __name__ == "__main__":
    main()
