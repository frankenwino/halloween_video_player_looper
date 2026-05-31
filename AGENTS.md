# AGENTS.md

<!-- tags: navigation, architecture, conventions -->

## Project Overview

Raspberry Pi video looper for Halloween displays. Loops video files fullscreen using VLC (`python-vlc`). Python 3.11+ with TOML config and CLI overrides.

**Entry point**: `halloween_video_player_looper/__main__.py` → `main()`
**CLI**: `halloween-video-looper [--config PATH] [-v VIDEO] [-r] [-s SLEEP] [-t] [-d DIR]`

## Directory Map

```
halloween_video_player_looper/   # Application package
├── __main__.py                  # Entry: args → config → select video → player → loop
├── config.py                    # Config dataclass + TOML loading + CLI merge
├── discovery.py                 # Video discovery via python-magic MIME detection
├── player.py                    # VideoPlayer: VLC wrapper with loop + orientation
└── video/                       # Bundled sample video
tests/                           # pytest suite (26 tests, 92% coverage)
├── conftest.py                  # Shared fixtures + VLC/magic mocks
├── test_config.py
├── test_discovery.py
├── test_player.py
└── test_integration.py
```

## Key Entry Points

| What | Where |
|------|-------|
| Application | `halloween_video_player_looper/__main__.py` |
| Configuration | `halloween_video_player_looper/config.py` → `Config` dataclass |
| Video discovery | `halloween_video_player_looper/discovery.py` → `discover_videos()` |
| Playback | `halloween_video_player_looper/player.py` → `VideoPlayer.play_loop()` |
| Example config | `config.example.toml` |

## Architecture

1. Parse CLI args → load TOML config → merge (CLI overrides TOML)
2. Select video: specific path (`-v`) or random from directory
3. Create VLC player with fullscreen/orientation settings
4. Loop: `play()` → poll `get_state()` until Ended → `stop()` → sleep → repeat
5. `KeyboardInterrupt` → `player.stop()` (releases VLC)

No threading — VLC handles playback internally, main thread polls state.

## Patterns That Deviate from Defaults

- **Lazy VLC import** in `player.py` — catches ImportError at module level for clear error if VLC missing
- **CLI overrides config** — non-None CLI values replace TOML values via dict merge
- **MIME-based video detection** — python-magic (libmagic), not file extensions
- **Package-relative video dir** — `Path(__file__).parent / "video"` not CWD
- **Orientation via VLC transform filter** — `--video-filter=transform`

## Error Handling

| Scenario | Result |
|----------|--------|
| VLC not installed | CRITICAL, exit |
| No videos found | CRITICAL, exit |
| Video dir missing | CRITICAL, exit |
| Specified file not video | CRITICAL, exit |
| Invalid TOML | ERROR, exit |
| VLC playback error | ERROR, break loop |

## Testing

All VLC and python-magic mocked at `sys.modules` level. Tests run anywhere without VLC or display.

## Detailed Documentation

See `.agents/summary/index.md` for full documentation index.

## Custom Instructions
<!-- This section is for human and agent-maintained operational knowledge.
     Add repo-specific conventions, gotchas, and workflow rules here.
     This section is preserved exactly as-is when re-running codebase-summary. -->
