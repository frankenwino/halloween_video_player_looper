"""Entry point for halloween-video-looper."""

import argparse
import logging
import random
import sys
from pathlib import Path

from .config import load_config
from .discovery import discover_videos, is_video
from .player import VideoPlayer


def main() -> None:
    args = _parse_args()
    config = load_config(args.config, _cli_overrides(args))
    _setup_logging(config.log_level)

    video = _select_video(config)

    player = VideoPlayer(config.fullscreen, (config.window_width, config.window_height), config.orientation)
    try:
        player.play_loop(video, config.sleep_seconds)
    except KeyboardInterrupt:
        logging.getLogger(__name__).info("Interrupted. Shutting down...")
        player.stop()


def _select_video(config) -> Path:
    """Determine which video to play."""
    logger = logging.getLogger(__name__)

    if config.video_path:
        path = config.video_path
        if not path.is_file():
            logger.critical("Video file does not exist: %s", path)
            sys.exit(1)
        if not is_video(path):
            logger.critical("File is not a video: %s", path)
            sys.exit(1)
        return path

    videos = discover_videos(config.video_dir)
    video = random.choice(videos)
    logger.info("Selected: %s", video.name)
    return video


def _cli_overrides(args: argparse.Namespace) -> dict:
    """Extract CLI overrides as a dict (None = not specified)."""
    overrides = {}
    if args.video:
        overrides["video_path"] = Path(args.video)
    if args.random:
        overrides["random_mode"] = True
    if args.sleep is not None:
        overrides["sleep_seconds"] = args.sleep
    if args.test:
        overrides["fullscreen"] = False
    if args.video_dir:
        overrides["video_dir"] = Path(args.video_dir)
    return overrides


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="halloween-video-looper",
        description="Loop video files for Halloween displays",
    )
    parser.add_argument("--config", type=Path, default=None, help="Path to config.toml")
    parser.add_argument("-v", "--video", type=str, default=None, help="Specific video file to loop")
    parser.add_argument("-r", "--random", action="store_true", help="Select random video from directory")
    parser.add_argument("-s", "--sleep", type=float, default=None, help="Seconds to pause between loops")
    parser.add_argument("-t", "--test", action="store_true", help="Run in windowed test mode")
    parser.add_argument("-d", "--video-dir", type=str, default=None, help="Video directory path")
    return parser.parse_args()


def _setup_logging(level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


if __name__ == "__main__":
    main()
