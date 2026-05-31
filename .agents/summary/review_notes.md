# Review Notes

## Consistency Check

✅ All documentation files reference the same module structure and API signatures.
✅ Config fields consistent across docs.
✅ VLC as video player referenced consistently.

## Completeness Check

### Well Documented
- Configuration system (TOML + CLI overrides)
- Video discovery workflow
- Playback loop mechanism
- Error handling strategy

### Gaps Identified

| Area | Gap | Recommendation |
|------|-----|----------------|
| Systemd service | No docs on running at boot | Add example .service file |
| Multiple videos | No playlist/shuffle-all mode | Consider adding playlist support |
| Audio output | No config for audio device | Add VLC audio output option |
| Video format support | No docs on which formats VLC handles | Document common formats |

## Recommendations

1. **Add systemd service file** — users will want auto-start on boot
2. **Add playlist mode** — shuffle through all videos instead of looping one
3. **Document VLC format support** — MP4, AVI, MKV, etc.
4. **Add `--duration` flag** — stop after N loops or N minutes
