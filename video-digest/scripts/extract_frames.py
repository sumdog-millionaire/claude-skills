"""Extract frames from a video for reading — every moment the picture changed, plus a sweep."""

import argparse
import re
import subprocess
from pathlib import Path

# The sweep lands a frame every half second because disk is free and reading is
# not. Only a fraction get read: the scene changes, plus whatever the transcript
# points at.
INTERVAL_SECONDS = 0.5

# Ceiling on the sweep only. A half-second sweep of a forty-minute tutorial is
# 4,800 files, so past a couple of minutes the interval widens to stay inside
# this. Scene changes are never thinned - they are the reading list.
MAX_SWEEP_FRAMES = 240

# Frames are scaled down because reading cost scales with area, and 576px is
# still wide enough to read a URL or a terminal command off a phone-shaped video.
FRAME_WIDTH = 576

# How different two frames must be before it counts as a change. 0.25 fires when
# a new caption appears over a talking head, but not on every blink and gesture.
SCENE_THRESHOLD = 0.25


def duration_seconds(video: Path) -> float:
    """Return the video's duration in seconds."""
    result = subprocess.run(
        [
            "ffprobe",
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


def rename_by_time(frames_dir: Path, pattern: str, times: list[float]) -> list[Path]:
    """Rename ffmpeg's sequential output to the moment each frame came from.

    Args:
        frames_dir: directory holding the sequentially-named frames.
        pattern: glob matching them, e.g. `sweep_*.png`.
        times: the moment each frame came from, in the same order.

    Returns:
        The renamed frame paths, in time order.
    """
    renamed = []
    for sequential, seconds in zip(sorted(frames_dir.glob(pattern)), times):
        stamped = frames_dir / f"t{seconds:07.1f}.png"
        sequential.replace(stamped)
        renamed.append(stamped)
    return renamed


def scene_frames(video: Path, frames_dir: Path, threshold: float = SCENE_THRESHOLD) -> list[Path]:
    """Write a frame at every moment the picture changed significantly.

    One pass does both jobs: `select` keeps only the changed frames and `showinfo`
    reports, on stderr, the moment each one came from. Extracting at the exact
    moment matters - on a long video the sweep is far too coarse to land near a
    caption that was only up for a second.
    """
    result = subprocess.run(
        [
            "ffmpeg",
            "-hide_banner",
            "-i",
            str(video),
            "-vf",
            f"select='gt(scene,{threshold})',scale={FRAME_WIDTH}:-1,showinfo",
            # Without vfr, ffmpeg pads the dropped frames back in at a constant rate.
            "-fps_mode",
            "vfr",
            str(frames_dir / "scene_%04d.png"),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    times = [round(float(t), 1) for t in re.findall(r"pts_time:([0-9.]+)", result.stderr)]
    return rename_by_time(frames_dir, "scene_*.png", times)


def sweep_frames(video: Path, frames_dir: Path, interval: float) -> list[Path]:
    """Write a frame every `interval` seconds, catching whatever the scene pass stepped over."""
    subprocess.run(
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(video),
            "-vf",
            f"fps=1/{interval},scale={FRAME_WIDTH}:-1",
            str(frames_dir / "sweep_%04d.png"),
        ],
        check=True,
    )
    count = len(list(frames_dir.glob("sweep_*.png")))
    return rename_by_time(frames_dir, "sweep_*.png", [n * interval for n in range(count)])


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract frames and find scene changes.")
    parser.add_argument("video", type=Path, help="Path to the downloaded video file.")
    parser.add_argument("--interval", type=float, default=INTERVAL_SECONDS)
    parser.add_argument("--max-sweep-frames", type=int, default=MAX_SWEEP_FRAMES)
    parser.add_argument(
        "--frames-dir",
        type=Path,
        default=None,
        help="Where to write frames (default: a frames/ folder beside the video). "
        "Point this at the run folder when the video itself is staying put, "
        "such as a local recording that is not being copied anywhere.",
    )
    args = parser.parse_args()

    frames_dir = args.frames_dir or args.video.with_name("frames")
    frames_dir.mkdir(parents=True, exist_ok=True)
    for stale in frames_dir.glob("*.png"):
        stale.unlink()

    duration = duration_seconds(args.video)
    interval = max(args.interval, duration / args.max_sweep_frames)

    changes = scene_frames(args.video, frames_dir)
    # The sweep runs second so a coarse sweep frame never overwrites an exact
    # scene frame that landed on the same timestamp.
    sweep = sweep_frames(args.video, frames_dir, interval)
    total = len(set(changes) | set(sweep))

    print(f"{duration:.1f}s video | {total} frames in {frames_dir}, named by timestamp")
    print(f"sweep every {interval:.1f}s ({len(sweep)} frames)")
    print(f"\npicture changed at {len(changes)} moments - read these first:")
    for frame in changes:
        print(f"  {frame.name}")


if __name__ == "__main__":
    main()
