"""Extract dense, timestamped frames and time-ranged contact sheets from a meeting recording."""

import argparse
import os
import re
import shutil
import subprocess
from pathlib import Path

INTERVAL_SECONDS = 3.0
FRAME_WIDTH = 1280
SCENE_THRESHOLD = 0.05
CONTACT_SHEET_COLUMNS = 4
CONTACT_SHEET_ROWS = 5
CONTACT_FRAME_WIDTH = 320


def find_binary(name: str) -> Path:
    """Return an ffmpeg-suite executable, including a Windows winget fallback."""
    executable = shutil.which(name)
    if executable:
        return Path(executable)

    if os.name == "nt":
        local_app_data = Path(os.environ["LOCALAPPDATA"])
        pattern = f"Microsoft/WinGet/Packages/Gyan.FFmpeg_*/ffmpeg-*/bin/{name}.exe"
        matches = sorted(local_app_data.glob(pattern), reverse=True)
        if matches:
            return matches[0]

    raise FileNotFoundError(f"{name} is not available. Install ffmpeg, then open a new shell.")


def parse_timestamp(value: str) -> float:
    """Convert seconds or an HH:MM:SS.s timestamp to seconds."""
    if ":" not in value:
        return float(value)

    parts = [float(part) for part in value.split(":")]
    if len(parts) > 3:
        raise ValueError(f"Invalid timestamp: {value}")
    while len(parts) < 3:
        parts.insert(0, 0.0)
    hours, minutes, seconds = parts
    if minutes >= 60 or seconds >= 60:
        raise ValueError(f"Invalid timestamp: {value}")
    return hours * 3600 + minutes * 60 + seconds


def frame_timestamp(seconds: float) -> str:
    """Format seconds for a timestamped frame filename."""
    return f"{seconds:08.1f}"


def duration_seconds(video: Path, ffprobe: Path) -> float:
    """Return the recording duration in seconds."""
    result = subprocess.run(
        [
            str(ffprobe),
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(video),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return float(result.stdout.strip())


def rename_regular_frames(frames_dir: Path, interval: float) -> list[Path]:
    """Rename sequential regular frames with their recording timestamps."""
    frames = sorted(frames_dir.glob("regular_*.jpg"))
    renamed: list[Path] = []
    for index, frame in enumerate(frames):
        target = frames_dir / f"t{index * interval:08.1f}.jpg"
        frame.replace(target)
        renamed.append(target)
    return renamed


def extract_regular_frames(
    video: Path,
    frames_dir: Path,
    ffmpeg: Path,
    interval: float,
    width: int,
) -> list[Path]:
    """Extract a readable frame at a fixed interval across the full meeting."""
    subprocess.run(
        [
            str(ffmpeg),
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(video),
            "-vf",
            f"fps=1/{interval},scale={width}:-2",
            "-q:v",
            "3",
            str(frames_dir / "regular_%05d.jpg"),
        ],
        check=True,
    )
    return rename_regular_frames(frames_dir, interval)


def extract_change_frames(
    video: Path,
    frames_dir: Path,
    ffmpeg: Path,
    threshold: float,
    width: int,
) -> list[Path]:
    """Extract extra frames when the screen changes between regular samples."""
    result = subprocess.run(
        [
            str(ffmpeg),
            "-hide_banner",
            "-i",
            str(video),
            "-vf",
            f"select='gt(scene,{threshold})',scale={width}:-2,showinfo",
            "-fps_mode",
            "vfr",
            "-q:v",
            "3",
            str(frames_dir / "change_%05d.jpg"),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    times = [round(float(value), 1) for value in re.findall(r"pts_time:([0-9.]+)", result.stderr)]
    frames = sorted(frames_dir.glob("change_*.jpg"))
    renamed: list[Path] = []
    for frame, seconds in zip(frames, times):
        target = frames_dir / f"change_t{seconds:08.1f}.jpg"
        frame.replace(target)
        renamed.append(target)
    return renamed


def extract_requested_frame(
    video: Path,
    frames_dir: Path,
    ffmpeg: Path,
    seconds: float,
    width: int,
) -> Path:
    """Extract one exact frame without changing the existing frame set."""
    if seconds < 0:
        raise ValueError("Requested timestamps cannot be negative")
    target = frames_dir / f"requested_t{frame_timestamp(seconds)}.jpg"
    subprocess.run(
        [
            str(ffmpeg),
            "-hide_banner",
            "-loglevel",
            "error",
            "-ss",
            f"{seconds:.3f}",
            "-i",
            str(video),
            "-frames:v",
            "1",
            "-vf",
            f"scale={width}:-2",
            "-q:v",
            "2",
            "-y",
            str(target),
        ],
        check=True,
    )
    return target


def extract_contact_sheets(
    video: Path,
    sheets_dir: Path,
    ffmpeg: Path,
    interval: float,
) -> list[Path]:
    """Build time-ranged one-minute contact sheets for efficient chronological review."""
    frames_per_sheet = CONTACT_SHEET_COLUMNS * CONTACT_SHEET_ROWS
    seconds_per_sheet = interval * frames_per_sheet
    filter_graph = (
        f"fps=1/{interval},scale={CONTACT_FRAME_WIDTH}:-2,"
        f"tile={CONTACT_SHEET_COLUMNS}x{CONTACT_SHEET_ROWS}:"
        f"nb_frames={frames_per_sheet}:padding=4:margin=4"
    )
    subprocess.run(
        [
            str(ffmpeg),
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(video),
            "-vf",
            filter_graph,
            "-fps_mode",
            "vfr",
            "-q:v",
            "3",
            str(sheets_dir / "sheet_%04d.jpg"),
        ],
        check=True,
    )

    sheets = sorted(sheets_dir.glob("sheet_*.jpg"))
    renamed: list[Path] = []
    for index, sheet in enumerate(sheets):
        start = round(index * seconds_per_sheet)
        end = round((index + 1) * seconds_per_sheet - interval)
        target = sheets_dir / f"sheet_{start:05d}-{end:05d}.jpg"
        sheet.replace(target)
        renamed.append(target)
    return renamed


def clear_outputs(frames_dir: Path, sheets_dir: Path) -> None:
    """Remove outputs from a previous extraction without touching other files."""
    for pattern in ("t*.jpg", "change_t*.jpg", "regular_*.jpg", "change_*.jpg"):
        for stale in frames_dir.glob(pattern):
            stale.unlink()
    for stale in sheets_dir.glob("sheet_*.jpg"):
        stale.unlink()


def main() -> None:
    """Extract dense meeting frames and print an extraction summary."""
    parser = argparse.ArgumentParser(description="Extract dense frames from a meeting recording.")
    parser.add_argument("video", type=Path, help="Path to the meeting recording.")
    parser.add_argument("--frames-dir", type=Path, required=True, help="Folder for frames and contact sheets.")
    parser.add_argument("--interval", type=float, default=INTERVAL_SECONDS, help="Seconds between regular frames.")
    parser.add_argument("--width", type=int, default=FRAME_WIDTH, help="Width of individual frames in pixels.")
    parser.add_argument(
        "--at",
        action="append",
        default=[],
        metavar="TIMESTAMP",
        help="Extract only an additional exact frame at seconds or HH:MM:SS.s. Repeat for several frames.",
    )
    parser.add_argument(
        "--scene-threshold",
        type=float,
        default=SCENE_THRESHOLD,
        help="Full-frame difference needed to save an extra screen-change frame.",
    )
    args = parser.parse_args()

    if args.interval <= 0:
        raise ValueError("--interval must be greater than zero")
    if args.width <= 0:
        raise ValueError("--width must be greater than zero")
    if not 0 < args.scene_threshold <= 1:
        raise ValueError("--scene-threshold must be between zero and one")

    video = args.video.resolve()
    if not video.is_file():
        raise FileNotFoundError(f"Recording not found: {video}")

    frames_dir = args.frames_dir.resolve()
    frames_dir.mkdir(parents=True, exist_ok=True)
    ffmpeg = find_binary("ffmpeg")

    if args.at:
        requested = [
            extract_requested_frame(video, frames_dir, ffmpeg, parse_timestamp(value), args.width)
            for value in args.at
        ]
        for frame in requested:
            print(frame)
        return

    sheets_dir = frames_dir / "contact-sheets"
    sheets_dir.mkdir(parents=True, exist_ok=True)
    clear_outputs(frames_dir, sheets_dir)

    ffprobe = find_binary("ffprobe")
    duration = duration_seconds(video, ffprobe)
    regular = extract_regular_frames(video, frames_dir, ffmpeg, args.interval, args.width)
    changes = extract_change_frames(video, frames_dir, ffmpeg, args.scene_threshold, args.width)
    sheets = extract_contact_sheets(video, sheets_dir, ffmpeg, args.interval)

    print(f"{duration:.1f}s recording")
    print(f"{len(regular)} regular frames every {args.interval:g}s")
    print(f"{len(changes)} additional screen-change frames")
    print(f"{len(sheets)} time-ranged contact sheets")
    print(f"frames: {frames_dir}")


if __name__ == "__main__":
    main()
