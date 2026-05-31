# AGENTS.md

<!-- tags: navigation, architecture, conventions, gotchas -->

## Project Overview

Raspberry Pi video looper for Halloween displays. Loops video files using OMXPlayer (D-Bus control). Single-file procedural Python script with argparse CLI.

**Critical**: OMXPlayer was removed from Pi OS Bullseye (2021). This app only works on Pi OS Buster or earlier.

**Entry point**: `python app/halloween_video_player_looper.py [flags]`

## Directory Map

```
app/                              # ALL application code
├── halloween_video_player_looper.py  # Main: CLI + video discovery + playback loop
├── video_duration.py             # Orphaned ffprobe utility (never imported)
├── __init__.py                   # Package metadata
└── video/                        # Default video directory (1 sample MP4)
tests/                            # Placeholder stubs (no real tests)
docs/                             # Sphinx stubs
```

## Key Entry Points

| What | Where |
|------|-------|
| Main application | `app/halloween_video_player_looper.py` (direct execution) |
| CLI flags | `-v VIDEO`, `-r` (random), `-s SLEEP` (minutes), `-t` (test/windowed) |
| Video directory | `./video/` relative to CWD (not package) |

## Architecture

Procedural script — no classes. Functions called from `if __name__ == "__main__"`:
1. Parse args → validate → discover videos → launch OMXPlayer
2. Playback loop: `play()` → `sleep(duration)` → `pause()` → `seek(0)` → repeat
3. Single OMXPlayer instance reused (avoids process restart overhead)

## Known Bugs and Gotchas

<!-- tags: bugs, gotchas -->

- **OMXPlayer is dead**: Removed from Pi OS Bullseye+. App cannot run on modern Pi OS.
- **Package structure broken**: `setup.py` uses `find_packages(include=['halloween_video_player_looper'])` but code is in `app/`. pip install won't work.
- **Error message bug**: Line ~170 `format(args.video)` — missing `current_time()` as first positional arg.
- **CWD-dependent paths**: `os.path.abspath("video")` resolves from wherever you run the script, not from the package location.
- **Python version mismatch**: Declares 2.7 support but `video_duration.py` uses f-strings (3.6+).
- **Hardcoded display settings**: 180° orientation, 720×360 test window — no config file.
- **No error handling**: OMXPlayer D-Bus failures produce unhelpful tracebacks.

## Dependencies

**Runtime** (requirements.txt):
- `omxplayer-wrapper` — OMXPlayer D-Bus bindings (deprecated)
- `python-magic` — libmagic MIME detection
- `dbus-python` — D-Bus communication

**System binaries**: `omxplayer` (deprecated), `libmagic1`, D-Bus daemon

## Patterns That Deviate from Defaults

- MIME-based video detection via libmagic (not file extensions)
- OMXPlayer controlled via D-Bus (not subprocess stdin/stdout)
- Display orientation hardcoded to 180° (mounted upside-down)
- `sys.exit()` for all error paths (no exceptions, no return codes)

## Detailed Documentation

See `.agents/summary/index.md` for full documentation index.

## Custom Instructions
<!-- This section is for human and agent-maintained operational knowledge.
     Add repo-specific conventions, gotchas, and workflow rules here.
     This section is preserved exactly as-is when re-running codebase-summary. -->
