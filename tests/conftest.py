"""Shared test fixtures."""

import sys
from unittest.mock import MagicMock

import pytest
from pathlib import Path

# Ensure hardware mocks are available
sys.modules.setdefault("vlc", MagicMock())
sys.modules.setdefault("magic", MagicMock())


@pytest.fixture
def tmp_video_dir(tmp_path):
    """Create a temp directory with a fake video file."""
    video_dir = tmp_path / "video"
    video_dir.mkdir()
    (video_dir / "spooky.mp4").write_bytes(b"fake video")
    return video_dir


@pytest.fixture
def sample_config(tmp_video_dir):
    """Config with temp video directory."""
    from halloween_video_player_looper.config import Config

    return Config(video_dir=tmp_video_dir, sleep_seconds=0)
