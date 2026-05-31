"""Configuration loading and validation."""

import logging
import sys
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

logger = logging.getLogger(__name__)

VALID_ORIENTATIONS = (0, 90, 180, 270)


@dataclass
class Config:
    """Application configuration with sensible defaults."""

    video_dir: Path = field(default_factory=lambda: Path(__file__).parent / "video")
    video_path: Path | None = None
    random_mode: bool = False
    sleep_seconds: float = 0
    fullscreen: bool = True
    window_width: int = 720
    window_height: int = 480
    orientation: int = 0
    log_level: str = "INFO"


def load_config(config_path: Path | None = None, cli_overrides: dict | None = None) -> Config:
    """Load config from TOML file, then apply CLI overrides."""
    if config_path and config_path.exists():
        try:
            with open(config_path, "rb") as f:
                data = tomllib.load(f)
        except tomllib.TOMLDecodeError as e:
            logger.error("Invalid config file %s: %s", config_path, e)
            sys.exit(1)
    else:
        data = {}

    video = data.get("video", {})
    playback = data.get("playback", {})
    app = data.get("app", {})

    config = Config(
        video_dir=Path(video["directory"]) if "directory" in video else Config().video_dir,
        video_path=Path(video["path"]) if "path" in video else None,
        sleep_seconds=playback.get("sleep_seconds", Config.sleep_seconds),
        fullscreen=playback.get("fullscreen", Config.fullscreen),
        window_width=playback.get("window_width", Config.window_width),
        window_height=playback.get("window_height", Config.window_height),
        orientation=playback.get("orientation", Config.orientation),
        log_level=app.get("log_level", Config.log_level),
    )

    # Apply CLI overrides (non-None values)
    if cli_overrides:
        for key, value in cli_overrides.items():
            if value is not None and hasattr(config, key):
                object.__setattr__(config, key, value)

    _validate(config)
    return config


def _validate(config: Config) -> None:
    """Validate config values, exit on failure."""
    if config.orientation not in VALID_ORIENTATIONS:
        logger.error("Orientation must be one of %s, got %s", VALID_ORIENTATIONS, config.orientation)
        sys.exit(1)
    if config.sleep_seconds < 0:
        logger.error("Sleep seconds must be >= 0, got %s", config.sleep_seconds)
        sys.exit(1)
