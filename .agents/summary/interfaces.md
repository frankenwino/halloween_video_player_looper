# Interfaces

## CLI Interface

```
halloween-video-looper [OPTIONS]
```

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--config` | Path | None | Path to TOML config file |
| `-v`, `--video` | str | None | Specific video file to loop |
| `-r`, `--random` | flag | False | Random video from directory |
| `-s`, `--sleep` | float | None | Seconds between loops |
| `-t`, `--test` | flag | False | Windowed mode |
| `-d`, `--video-dir` | str | None | Video directory path |

## Configuration (TOML)

```toml
[video]
directory = "/path/to/videos"
path = "/path/to/specific.mp4"

[playback]
sleep_seconds = 0
fullscreen = true
window_width = 720
window_height = 480
orientation = 0

[app]
log_level = "INFO"
```

## Python APIs

```python
# Config
load_config(config_path: Path | None, cli_overrides: dict | None) -> Config

# Discovery
is_video(file_path: Path) -> bool
discover_videos(video_dir: Path) -> list[Path]

# Player
VideoPlayer(fullscreen: bool, window_size: tuple[int, int], orientation: int)
VideoPlayer.play_loop(video_path: Path, sleep_seconds: float) -> None
VideoPlayer.stop() -> None
```
