# Interfaces

## CLI Interface

```
python app/halloween_video_player_looper.py [OPTIONS]
```

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `-v`, `--video` | string | None | Path to specific video file to loop |
| `-r`, `--random` | flag | False | Select random video from video directory |
| `-s`, `--sleep` | float | 0 | Minutes to pause between loop iterations |
| `-t`, `--test` | flag | False | Run in windowed test mode (720×360) |
| `-h`, `--help` | flag | — | Show help message |

**Mutual exclusivity** (not enforced): `-v` and `-r` are alternative modes. If neither is provided, the app prints help and exits.

## Function Signatures

```python
def current_time() -> str
def file_magic(file_path: str) -> tuple[str, str]
def is_video(file_path: str) -> bool
def generate_video_list(video_dir: str = os.path.abspath("video")) -> list[str]
def single_video_player_looper(video_clip_path: str, sleep_minutes: float, test_mode: bool) -> None
```

## OMXPlayer D-Bus Interface (External)

The app uses `omxplayer-wrapper` which communicates via D-Bus:

| Method | Purpose |
|--------|---------|
| `OMXPlayer(path, args=[...])` | Launch player process |
| `player.play()` | Resume playback |
| `player.pause()` | Pause playback |
| `player.duration()` | Get video duration in seconds |
| `player.set_position(0.0)` | Seek to beginning |
| `player.quit()` | Terminate player process |

## Filesystem Interface

- **Input**: Video files in `./video/` directory (or path specified via `-v`)
- **Output**: None (video displayed on HDMI)
- **Supported formats**: Any file with MIME type containing "video" (detected via libmagic)
