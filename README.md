# Halloween Video Player Looper

Loops video files on a Raspberry Pi for Halloween displays. Plays a video fullscreen on repeat with configurable pause between loops. Supports random video selection from a directory, windowed test mode, and display orientation.

## Requirements

- Raspberry Pi (any model with HDMI output) or Linux desktop
- VLC media player installed system-wide
- Python 3.11+
- HDMI-connected display

## Installation

```bash
# Install VLC (required)
sudo apt install vlc

# Clone the repository
git clone https://github.com/frankenwino/halloween_video_player_looper.git
cd halloween_video_player_looper

# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install the package
pip install -e .

# For development (includes pytest)
pip install -e ".[dev]"
```

## Configuration

The application works with sensible defaults. To customize, create a `config.toml`:

```toml
[video]
directory = "/home/pi/halloween-videos"
# path = "/path/to/specific/video.mp4"  # Overrides directory

[playback]
sleep_seconds = 0        # Pause between loops
fullscreen = true
window_width = 720       # Used in test/windowed mode
window_height = 480
orientation = 0          # 0, 90, 180, 270 degrees

[app]
log_level = "INFO"       # DEBUG, INFO, WARNING, ERROR
```

## Usage

```bash
# Play a random video from the default directory
halloween-video-looper

# Play a specific video
halloween-video-looper -v /path/to/video.mp4

# Random video with 5 second pause between loops
halloween-video-looper -r -s 5

# Windowed test mode (not fullscreen)
halloween-video-looper -t

# Use a custom video directory
halloween-video-looper -d /path/to/videos/

# Use a config file
halloween-video-looper --config /path/to/config.toml

# Stop with Ctrl+C
```

### CLI Flags

| Flag | Description |
|------|-------------|
| `--config PATH` | Path to config.toml |
| `-v`, `--video PATH` | Specific video file to loop |
| `-r`, `--random` | Select random video from directory |
| `-s`, `--sleep SECONDS` | Pause between loop iterations |
| `-t`, `--test` | Windowed mode (not fullscreen) |
| `-d`, `--video-dir PATH` | Video directory path |

## Running Tests

```bash
pytest
pytest -v
pytest --cov --cov-report=term-missing
```

## Troubleshooting

### VLC not found

```
CRITICAL: VLC not available
```

Install VLC: `sudo apt install vlc`

### No display / cannot open display

If running over SSH, VLC needs a display. Either:
- Run directly on the Pi (not over SSH)
- Set `DISPLAY=:0` environment variable
- Use `--test` mode for windowed playback

### No video files found

Ensure your video directory contains files with video MIME types (`.mp4`, `.avi`, `.mkv`, etc.). The app uses libmagic for detection, not file extensions.

### Permission errors

If VLC complains about permissions:
```bash
# Allow VLC to run as root (if needed on Pi)
sed -i 's/geteuid/getppid/' /usr/bin/vlc
```

Or run as a regular user (recommended).

## License

GNU General Public License v3 — see [LICENSE](LICENSE) for details.
