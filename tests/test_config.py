"""Tests for configuration loading and validation."""

import pytest
from pathlib import Path

from halloween_video_player_looper.config import Config, load_config


class TestConfigDefaults:
    def test_default_values(self):
        config = Config()
        assert config.sleep_seconds == 0
        assert config.fullscreen is True
        assert config.window_width == 720
        assert config.window_height == 480
        assert config.orientation == 0
        assert config.log_level == "INFO"
        assert config.video_path is None
        assert config.random_mode is False

    def test_default_video_dir_is_package_relative(self):
        config = Config()
        assert config.video_dir.name == "video"
        assert "halloween_video_player_looper" in str(config.video_dir)


class TestLoadConfig:
    def test_missing_file_returns_defaults(self):
        config = load_config(Path("/nonexistent/config.toml"))
        assert config.orientation == 0

    def test_none_path_returns_defaults(self):
        config = load_config(None)
        assert config == Config()

    def test_valid_toml(self, tmp_path):
        toml_file = tmp_path / "config.toml"
        toml_file.write_text('[playback]\nsleep_seconds = 5\norientation = 180\nfullscreen = false\n')
        config = load_config(toml_file)
        assert config.sleep_seconds == 5
        assert config.orientation == 180
        assert config.fullscreen is False

    def test_invalid_toml_exits(self, tmp_path):
        toml_file = tmp_path / "bad.toml"
        toml_file.write_text("invalid[[[toml")
        with pytest.raises(SystemExit):
            load_config(toml_file)

    def test_cli_overrides(self, tmp_path):
        toml_file = tmp_path / "config.toml"
        toml_file.write_text('[playback]\nsleep_seconds = 5\n')
        config = load_config(toml_file, cli_overrides={"sleep_seconds": 10})
        assert config.sleep_seconds == 10

    def test_cli_none_does_not_override(self, tmp_path):
        toml_file = tmp_path / "config.toml"
        toml_file.write_text('[playback]\nsleep_seconds = 5\n')
        config = load_config(toml_file, cli_overrides={"sleep_seconds": None})
        assert config.sleep_seconds == 5

    def test_invalid_orientation_exits(self, tmp_path):
        toml_file = tmp_path / "config.toml"
        toml_file.write_text('[playback]\norientation = 45\n')
        with pytest.raises(SystemExit):
            load_config(toml_file)

    def test_negative_sleep_exits(self, tmp_path):
        toml_file = tmp_path / "config.toml"
        toml_file.write_text('[playback]\nsleep_seconds = -1\n')
        with pytest.raises(SystemExit):
            load_config(toml_file)
