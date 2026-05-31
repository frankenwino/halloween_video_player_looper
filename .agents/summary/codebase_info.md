# Codebase Information

## Project Identity

- **Name**: halloween_video_player_looper
- **Version**: 0.1.0
- **License**: GNU General Public License v3
- **Python**: Targets 2.7 and 3.5–3.8 (declared), actually requires Python 3 (f-strings in video_duration.py)
- **Author**: Andy Browne

## Technology Stack

| Layer | Technology |
|-------|-----------|
| Language | Python (mixed 2/3 compatibility issues) |
| Video playback | OMXPlayer via `omxplayer-wrapper` (D-Bus) |
| File detection | `python-magic` (libmagic) |
| D-Bus | `dbus-python` |
| CLI | argparse (stdlib) |
| Build | setuptools (legacy setup.py) |
| Testing | tox + unittest (placeholder only) |

## Directory Structure

```
halloween_video_player_looper/
├── app/                           # Application code
│   ├── halloween_video_player_looper.py  # Main module (CLI + logic)
│   ├── video_duration.py          # Orphaned ffprobe utility
│   ├── __init__.py                # Package metadata
│   └── video/                     # Default video directory
│       └── Graveyard - Landscape - 16s.mp4
├── tests/                         # Placeholder tests (no assertions)
├── docs/                          # Sphinx documentation stubs
├── setup.py                       # Legacy packaging (broken package discovery)
├── setup.cfg                      # bump2version + flake8 config
├── tox.ini                        # Multi-version test config
├── Makefile                       # Cookiecutter targets
├── requirements.txt               # Runtime dependencies
├── README.md                      # Brief project description
├── README.rst                     # Cookiecutter template README
└── AGENTS.md                      # AI assistant context
```

## Entry Points

| Entry Point | Location | Purpose |
|-------------|----------|---------|
| Direct execution | `python app/halloween_video_player_looper.py` | Run from repo root |
| CLI arguments | `-v VIDEO`, `-r`, `-s SLEEP`, `-t` | Video selection and playback options |

## Target Platform

- Raspberry Pi (any model with HDMI output)
- Raspberry Pi OS **Buster or earlier** (OMXPlayer removed in Bullseye)
- HDMI-connected display
- D-Bus daemon running
