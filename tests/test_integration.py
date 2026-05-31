"""Integration tests — full application flow with mocked VLC and magic."""

import sys
from unittest.mock import MagicMock, patch
from pathlib import Path

import pytest

from halloween_video_player_looper.config import Config, load_config


class TestIntegrationVideoSelection:
    def test_specific_video_path(self, tmp_path):
        video = tmp_path / "test.mp4"
        video.write_bytes(b"fake")

        mock_magic = sys.modules["magic"]
        mock_magic.from_file.return_value = "video/mp4"

        config = Config(video_path=video, video_dir=tmp_path)

        from halloween_video_player_looper.__main__ import _select_video

        result = _select_video(config)
        assert result == video

    def test_random_from_directory(self, tmp_path):
        (tmp_path / "a.mp4").write_bytes(b"fake")
        (tmp_path / "b.mp4").write_bytes(b"fake")

        mock_magic = sys.modules["magic"]
        mock_magic.from_file.return_value = "video/mp4"

        config = Config(video_dir=tmp_path)

        from halloween_video_player_looper.__main__ import _select_video

        result = _select_video(config)
        assert result.suffix == ".mp4"

    def test_missing_video_path_exits(self, tmp_path):
        config = Config(video_path=tmp_path / "nonexistent.mp4")

        from halloween_video_player_looper.__main__ import _select_video

        with pytest.raises(SystemExit):
            _select_video(config)


class TestIntegrationConfigOverride:
    def test_cli_overrides_toml(self, tmp_path):
        toml_file = tmp_path / "config.toml"
        toml_file.write_text('[playback]\nsleep_seconds = 5\nfullscreen = true\n')

        config = load_config(toml_file, cli_overrides={"fullscreen": False, "sleep_seconds": 10})
        assert config.fullscreen is False
        assert config.sleep_seconds == 10
