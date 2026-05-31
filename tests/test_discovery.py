"""Tests for video discovery module."""

import sys
import pytest
from pathlib import Path

from halloween_video_player_looper.discovery import is_video, discover_videos


@pytest.fixture
def mock_magic():
    """Get the mocked magic module."""
    return sys.modules["magic"]


class TestIsVideo:
    def test_video_mime_returns_true(self, mock_magic):
        mock_magic.from_file.return_value = "video/mp4"
        assert is_video(Path("/fake/video.mp4")) is True

    def test_non_video_mime_returns_false(self, mock_magic):
        mock_magic.from_file.return_value = "text/plain"
        assert is_video(Path("/fake/notes.txt")) is False

    def test_error_returns_false(self, mock_magic):
        mock_magic.from_file.side_effect = OSError("no such file")
        assert is_video(Path("/fake/missing.mp4")) is False
        mock_magic.from_file.side_effect = None


class TestDiscoverVideos:
    def test_finds_video_files(self, tmp_path, mock_magic):
        (tmp_path / "clip.mp4").write_bytes(b"fake")
        (tmp_path / "notes.txt").write_text("not video")
        mock_magic.from_file.side_effect = lambda p, mime=False: "video/mp4" if "clip" in str(p) else "text/plain"

        videos = discover_videos(tmp_path)
        assert len(videos) == 1
        assert videos[0].name == "clip.mp4"
        mock_magic.from_file.side_effect = None

    def test_missing_dir_exits(self):
        with pytest.raises(SystemExit):
            discover_videos(Path("/nonexistent/dir"))

    def test_empty_dir_exits(self, tmp_path, mock_magic):
        mock_magic.from_file.return_value = "text/plain"
        (tmp_path / "readme.txt").write_text("no videos here")
        with pytest.raises(SystemExit):
            discover_videos(tmp_path)
        mock_magic.from_file.return_value = None
        mock_magic.from_file.side_effect = None
