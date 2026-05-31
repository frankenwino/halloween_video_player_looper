# Review Notes

## Consistency Check

✅ Documentation files reference the same functions and module structure consistently.
⚠️ `setup.py` declares package name `halloween_video_player_looper` but code lives in `app/` — package installation is broken.

## Completeness Check

### Well Documented
- CLI interface and flags
- Playback loop mechanism
- Video discovery workflow
- OMXPlayer D-Bus interaction pattern

### Gaps and Issues

| Area | Issue | Severity |
|------|-------|----------|
| OMXPlayer deprecation | App cannot run on Pi OS Bullseye+ (2021 onwards) | **Critical** |
| Package structure | `setup.py` won't find code in `app/` directory | High |
| Error message bug | Line ~170: `format(args.video)` missing `current_time()` | Medium |
| Path resolution | `os.path.abspath("video")` depends on CWD | Medium |
| Python version | Declares 2.7 support but `video_duration.py` uses f-strings | Medium |
| Orphaned code | `video_duration.py` never imported by main app | Low |
| Tests | Placeholder only — no assertions, no coverage | High |
| No error handling | OMXPlayer D-Bus failures crash without useful message | Medium |
| No logging | Uses `print()` throughout | Low |
| Hardcoded values | Orientation (180°), window size (720×360), video dir | Low |

## Recommendations

1. **Replace OMXPlayer** with `vlc` (python-vlc), `mpv` (python-mpv), or `ffplay` — OMXPlayer is dead
2. **Modernize to Python 3.11+** — drop 2.7/3.5 support, use pathlib, type hints, dataclasses
3. **Fix package structure** — move to `pyproject.toml`, proper package layout
4. **Add configuration** — TOML config file for orientation, window size, video directory
5. **Add real tests** — mock the video player, test discovery and CLI logic
6. **Add logging** — replace print statements
7. **Remove orphaned code** — delete or integrate `video_duration.py`
8. **Fix path resolution** — use package-relative or configurable paths
