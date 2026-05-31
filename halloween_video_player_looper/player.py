"""VLC video playback loop."""

import logging
import sys
import time
from pathlib import Path

try:
    import vlc
except (ImportError, OSError) as e:
    vlc = None
    _vlc_error = e

logger = logging.getLogger(__name__)


class VideoPlayer:
    """Loops a video file using VLC."""

    def __init__(self, fullscreen: bool, window_size: tuple[int, int], orientation: int) -> None:
        if vlc is None:
            logger.critical("VLC not available: %s", _vlc_error)
            sys.exit(1)

        vlc_args = ["--no-video-title-show"]
        if orientation:
            vlc_args.extend(["--video-filter=transform", f"--transform-type={_orientation_to_transform(orientation)}"])

        self._instance = vlc.Instance(vlc_args)
        self._player = self._instance.media_player_new()
        self._fullscreen = fullscreen
        self._window_size = window_size

        if fullscreen:
            self._player.set_fullscreen(True)

    def play_loop(self, video_path: Path, sleep_seconds: float) -> None:
        """Play video in a loop until KeyboardInterrupt."""
        media = self._instance.media_new(str(video_path))
        logger.info("Looping: %s (sleep %.1fs between loops)", video_path.name, sleep_seconds)

        while True:
            self._player.set_media(media)
            self._player.play()

            if self._fullscreen:
                self._player.set_fullscreen(True)

            # Wait for playback to start
            time.sleep(0.5)

            # Wait for playback to end
            while self._player.get_state() not in (vlc.State.Ended, vlc.State.Error):
                time.sleep(0.5)

            if self._player.get_state() == vlc.State.Error:
                logger.error("VLC playback error for %s", video_path.name)
                break

            logger.info("Playback ended. Sleeping %.1fs...", sleep_seconds)
            self._player.stop()

            if sleep_seconds > 0:
                time.sleep(sleep_seconds)

    def stop(self) -> None:
        """Stop playback and release resources."""
        self._player.stop()
        self._player.release()
        self._instance.release()
        logger.info("Player stopped.")


def _orientation_to_transform(degrees: int) -> str:
    """Convert degrees to VLC transform type string."""
    return {90: "90", 180: "180", 270: "270"}.get(degrees, "0")
