"""Video file discovery via MIME type detection."""

import logging
import sys
from pathlib import Path

import magic

logger = logging.getLogger(__name__)


def is_video(file_path: Path) -> bool:
    """Check if file has a video MIME type."""
    try:
        mime_type = magic.from_file(str(file_path), mime=True)
        return "video" in mime_type
    except (OSError, ValueError):
        return False


def discover_videos(video_dir: Path) -> list[Path]:
    """Find all video files in directory recursively."""
    if not video_dir.is_dir():
        logger.critical("Video directory does not exist: %s", video_dir)
        sys.exit(1)

    videos = sorted(p for p in video_dir.rglob("*") if p.is_file() and is_video(p))

    if not videos:
        logger.critical("No video files found in %s", video_dir)
        sys.exit(1)

    logger.info("Found %d video(s) in %s", len(videos), video_dir)
    return videos
