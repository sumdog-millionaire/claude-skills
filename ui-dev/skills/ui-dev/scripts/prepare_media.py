#!/usr/bin/env python3
"""Extract lossless video frames, prepare web sequences, or compress a muted hero."""

import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any


def binary(name: str) -> str:
    """Return an installed media binary or fail with a clear error."""
    path = shutil.which(name)
    if path is None:
        raise FileNotFoundError(f"{name} is required and was not found on PATH")
    return path


def run(command: list[str]) -> None:
    """Run one media command and expose any failure."""
    subprocess.run(command, check=True)


def probe(path: Path) -> dict[str, Any]:
    """Return measurements for the first video stream and its container."""
    result = subprocess.run(
        [
            binary("ffprobe"),
            "-v",
            "error",
            "-select_streams",
            "v:0",
            "-show_entries",
            "stream=width,height,avg_frame_rate,pix_fmt",
            "-show_entries",
            "format=duration,size",
            "-of",
            "json",
            str(path),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    data: dict[str, Any] = json.loads(result.stdout)
    stream = data["streams"][0]
    container = data["format"]
    duration = container.get("duration")
    rate = stream.get("avg_frame_rate", "0/0").split("/")
    fps = float(rate[0]) / float(rate[1]) if len(rate) == 2 and float(rate[1]) else None
    return {
        "width": int(stream["width"]),
        "height": int(stream["height"]),
        "duration_seconds": round(float(duration), 6) if duration not in (None, "N/A") else None,
        "average_fps": round(fps, 6) if fps is not None else None,
        "pixel_format": stream.get("pix_fmt"),
        "size_bytes": int(container.get("size", path.stat().st_size)),
    }


def frame_timestamps(path: Path) -> list[float | None]:
    """Return presentation timestamps for every decoded source frame."""
    result = subprocess.run(
        [
            binary("ffprobe"),
            "-v",
            "error",
            "-select_streams",
            "v:0",
            "-show_frames",
            "-show_entries",
            "frame=best_effort_timestamp_time",
            "-of",
            "json",
            str(path),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    frames: list[dict[str, str]] = json.loads(result.stdout)["frames"]
    return [
        round(float(frame["best_effort_timestamp_time"]), 6)
        if frame.get("best_effort_timestamp_time") not in (None, "N/A")
        else None
        for frame in frames
    ]


def scale_filter(width: int) -> str:
    """Scale down to the requested width without enlarging the source."""
    if width <= 0:
        raise ValueError("width must be greater than zero")
    return f"scale='min({width},iw)':-2:flags=lanczos"


def clear_frames(directory: Path) -> None:
    """Remove only outputs owned by this script before regenerating them."""
    for stale in (*directory.glob("frame_*.jpg"), *directory.glob("frame_*.png")):
        stale.unlink()
    (directory / "manifest.json").unlink(missing_ok=True)


def prepare_hero(source: Path, output: Path, poster: Path | None, width: int, crf: int) -> None:
    """Write a muted, streamable H.264 hero video and optional poster."""
    if output.suffix.lower() != ".mp4":
        raise ValueError("hero output must use the .mp4 extension")
    if not 0 <= crf <= 51:
        raise ValueError("crf must be between 0 and 51")

    output.parent.mkdir(parents=True, exist_ok=True)
    run(
        [
            binary("ffmpeg"),
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(source),
            "-map",
            "0:v:0",
            "-an",
            "-vf",
            scale_filter(width),
            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-crf",
            str(crf),
            "-pix_fmt",
            "yuv420p",
            "-movflags",
            "+faststart",
            "-y",
            str(output),
        ]
    )

    if poster is not None:
        poster.parent.mkdir(parents=True, exist_ok=True)
        run(
            [
                binary("ffmpeg"),
                "-hide_banner",
                "-loglevel",
                "error",
                "-ss",
                "0.1",
                "-i",
                str(source),
                "-frames:v",
                "1",
                "-vf",
                scale_filter(width),
                "-q:v",
                "2",
                "-y",
                str(poster),
            ]
        )

    report = {"source": probe(source), "hero": probe(output), "poster": str(poster) if poster else None}
    print(json.dumps(report, indent=2))


def extract_frames(source: Path, output_dir: Path) -> None:
    """Write every decoded source frame at its original dimensions as lossless PNG."""
    output_dir.mkdir(parents=True, exist_ok=True)
    clear_frames(output_dir)
    run(
        [
            binary("ffmpeg"),
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(source),
            "-map",
            "0:v:0",
            "-fps_mode",
            "passthrough",
            "-compression_level",
            "6",
            "-y",
            str(output_dir / "frame_%06d.png"),
        ]
    )

    frames = sorted(output_dir.glob("frame_*.png"))
    timestamps = frame_timestamps(source)
    if len(frames) != len(timestamps):
        raise RuntimeError(
            f"extracted {len(frames)} frames but ffprobe reported {len(timestamps)} decoded frames"
        )

    manifest = {
        "source": str(source),
        "source_media": probe(source),
        "format": "png",
        "encoding": "lossless",
        "transformations": [],
        "original_dimensions": True,
        "frame_count": len(frames),
        "size_bytes": sum(frame.stat().st_size for frame in frames),
        "frames": [
            {"file": frame.name, "source_index": index, "timestamp_seconds": timestamps[index]}
            for index, frame in enumerate(frames)
        ],
    }
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({key: value for key, value in manifest.items() if key != "frames"}, indent=2))


def selected_indices(total: int, requested: int | None) -> list[int]:
    """Select all frames or an evenly spaced baseline including both endpoints."""
    if requested is None or requested >= total:
        return list(range(total))
    if requested <= 0:
        raise ValueError("frame-count must be greater than zero")
    if requested == 1:
        return [0]
    # ponytail: even spacing is the baseline; add a selection manifest when semantic choice is needed.
    return [round(index * (total - 1) / (requested - 1)) for index in range(requested)]


def concat_path(path: Path) -> str:
    """Quote an absolute path for FFmpeg's concat format."""
    return path.resolve().as_posix().replace("'", "'\\''")


def optimise_frames(
    source_dir: Path,
    output_dir: Path,
    frame_count: int | None,
    width: int | None,
    quality: int,
    chroma_key: str | None,
    similarity: float,
    blend: float,
) -> None:
    """Create a smaller web sequence from a lossless extraction."""
    if not 2 <= quality <= 31:
        raise ValueError("quality must be between 2 (highest) and 31 (lowest)")
    if width is not None and width <= 0:
        raise ValueError("width must be greater than zero")
    if not 0 <= similarity <= 1 or not 0 <= blend <= 1:
        raise ValueError("similarity and blend must be between 0 and 1")
    if chroma_key is not None and re.fullmatch(r"[0-9A-Fa-f]{6}", chroma_key) is None:
        raise ValueError("chroma-key must be a six-digit hex colour such as 000000")

    source_manifest = json.loads((source_dir / "manifest.json").read_text(encoding="utf-8"))
    records: list[dict[str, Any]] = source_manifest["frames"]
    indices = selected_indices(len(records), frame_count)
    selected = [records[index] for index in indices]
    for record in selected:
        if not (source_dir / record["file"]).is_file():
            raise FileNotFoundError(f"master frame not found: {record['file']}")

    output_dir.mkdir(parents=True, exist_ok=True)
    clear_frames(output_dir)
    extension = "png" if chroma_key else "jpg"
    concat_file = output_dir / "selection.ffconcat"
    concat_file.write_text(
        "ffconcat version 1.0\n"
        + "".join(
            f"file '{concat_path(source_dir / record['file'])}'\nduration 1\n"
            for record in selected
        ),
        encoding="utf-8",
    )

    filters = []
    if width is not None:
        filters.append(scale_filter(width))
    if chroma_key:
        filters.extend([f"colorkey=0x{chroma_key}:{similarity:g}:{blend:g}", "format=rgba"])

    command = [
        binary("ffmpeg"),
        "-hide_banner",
        "-loglevel",
        "error",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(concat_file),
    ]
    if filters:
        command.extend(["-vf", ",".join(filters)])
    if extension == "jpg":
        command.extend(["-q:v", str(quality)])
    command.extend(["-fps_mode", "passthrough", "-y", str(output_dir / f"frame_%06d.{extension}")])
    try:
        run(command)
    finally:
        concat_file.unlink(missing_ok=True)

    outputs = sorted(output_dir.glob(f"frame_*.{extension}"))
    if len(outputs) != len(selected):
        raise RuntimeError(f"prepared {len(outputs)} frames but selected {len(selected)}")

    transformations = []
    if len(selected) != len(records):
        transformations.append(f"selected {len(selected)} of {len(records)} frames using even spacing")
    if width is not None:
        transformations.append(f"scaled down to a maximum width of {width}px")
    if chroma_key:
        transformations.append(f"removed pixels matching #{chroma_key.upper()} by flat-colour keying")
    if extension == "jpg":
        transformations.append(f"encoded as lossy JPEG at FFmpeg quality {quality}")

    manifest = {
        "source_manifest": str(source_dir / "manifest.json"),
        "format": extension,
        "encoding": "lossless" if extension == "png" else "lossy",
        "transformations": transformations,
        "selection": "all" if len(selected) == len(records) else "evenly_spaced",
        "source_frame_count": len(records),
        "frame_count": len(outputs),
        "width": probe(outputs[0])["width"],
        "height": probe(outputs[0])["height"],
        "size_bytes": sum(frame.stat().st_size for frame in outputs),
        "jpeg_quality": quality if extension == "jpg" else None,
        "chroma_key": f"#{chroma_key.upper()}" if chroma_key else None,
        "similarity": similarity if chroma_key else None,
        "blend": blend if chroma_key else None,
        "frames": [
            {
                "file": output.name,
                "source_file": record["file"],
                "source_index": record["source_index"],
                "timestamp_seconds": record["timestamp_seconds"],
            }
            for output, record in zip(outputs, selected, strict=True)
        ],
    }
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({key: value for key, value in manifest.items() if key != "frames"}, indent=2))


def parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""
    command = argparse.ArgumentParser(description=__doc__)
    subcommands = command.add_subparsers(dest="mode", required=True)

    extract = subcommands.add_parser("extract", help="extract every source frame as lossless PNG")
    extract.add_argument("source", type=Path)
    extract.add_argument("output_dir", type=Path, nargs="?")

    optimise = subcommands.add_parser("optimise", help="prepare a smaller sequence from extracted frames")
    optimise.add_argument("source_dir", type=Path)
    optimise.add_argument("output_dir", type=Path, nargs="?")
    optimise.add_argument("--frame-count", type=int)
    optimise.add_argument("--width", type=int)
    optimise.add_argument("--quality", type=int, default=5)
    optimise.add_argument("--chroma-key")
    optimise.add_argument("--similarity", type=float, default=0.12)
    optimise.add_argument("--blend", type=float, default=0.05)

    hero = subcommands.add_parser("hero", help="compress a muted hero MP4")
    hero.add_argument("source", type=Path)
    hero.add_argument("output", type=Path)
    hero.add_argument("--poster", type=Path)
    hero.add_argument("--width", type=int, default=1280)
    hero.add_argument("--crf", type=int, default=28)
    return command


def main() -> None:
    """Prepare the requested media output."""
    args = parser().parse_args()
    if args.mode == "extract":
        if not args.source.is_file():
            raise FileNotFoundError(f"source video not found: {args.source}")
        output_dir = args.output_dir or args.source.with_name(f"{args.source.stem}_frames")
        extract_frames(args.source, output_dir)
    elif args.mode == "optimise":
        if not args.source_dir.is_dir():
            raise FileNotFoundError(f"source frame directory not found: {args.source_dir}")
        output_dir = args.output_dir or args.source_dir.with_name(f"{args.source_dir.name}_web")
        optimise_frames(
            args.source_dir,
            output_dir,
            args.frame_count,
            args.width,
            args.quality,
            args.chroma_key,
            args.similarity,
            args.blend,
        )
    else:
        if not args.source.is_file():
            raise FileNotFoundError(f"source video not found: {args.source}")
        prepare_hero(args.source, args.output, args.poster, args.width, args.crf)


if __name__ == "__main__":
    main()
