# Codebase Information

## Project Identity

- **Name**: halloween-video-looper
- **Version**: 0.2.0
- **License**: GPL-3.0-or-later
- **Python**: ≥3.11
- **Author**: Andy Browne

## Technology Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.11+ |
| Video playback | VLC via `python-vlc` |
| File detection | `python-magic` (libmagic MIME) |
| Configuration | `tomllib` (stdlib) |
| CLI | `argparse` (stdlib) |
| Logging | `logging` (stdlib) |
| Build | hatchling |
| Testing | pytest, pytest-cov, pytest-mock |

## Directory Structure

```
halloween_video_player_looper/
├── halloween_video_player_looper/   # Application package
│   ├── __init__.py                  # Version metadata
│   ├── __main__.py                  # CLI entry point
│   ├── config.py                    # Config dataclass + TOML loading
│   ├── discovery.py                 # Video file discovery (python-magic)
│   ├── player.py                    # VideoPlayer (VLC wrapper)
│   └── video/                       # Bundled sample video
├── tests/                           # pytest suite
│   ├── conftest.py                  # Shared fixtures + mocks
│   ├── test_config.py              
│   ├── test_discovery.py           
│   ├── test_player.py             
│   └── test_integration.py        
├── pyproject.toml                   # Project metadata + build config
├── config.example.toml              # Example configuration
├── README.md                        # User documentation
├── AGENTS.md                        # AI assistant context
└── LICENSE                          # GPL-3.0
```

## Entry Points

| Entry Point | Location | Purpose |
|-------------|----------|---------|
| CLI command | `halloween-video-looper` | Installed script |
| Module execution | `python -m halloween_video_player_looper` | Direct invocation |
| Function | `halloween_video_player_looper.__main__:main` | Programmatic entry |

## Target Platform

- Raspberry Pi (any model with HDMI) or Linux desktop
- VLC installed system-wide (`apt install vlc`)
- HDMI-connected display
