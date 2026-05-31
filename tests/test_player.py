"""Tests for video player module."""

import sys
from unittest.mock import MagicMock, patch, PropertyMock
from pathlib import Path

import pytest

# Mock vlc before importing player
mock_vlc = MagicMock()
mock_vlc.State = MagicMock()
mock_vlc.State.Ended = "Ended"
mock_vlc.State.Error = "Error"
mock_vlc.State.Playing = "Playing"
sys.modules["vlc"] = mock_vlc


class TestVideoPlayer:
    @pytest.fixture(autouse=True)
    def reset_mocks(self):
        mock_vlc.Instance.reset_mock()

    def test_init_creates_vlc_instance(self):
        from halloween_video_player_looper.player import VideoPlayer

        player = VideoPlayer(fullscreen=True, window_size=(720, 480), orientation=0)
        mock_vlc.Instance.assert_called_once()
        assert player is not None

    def test_init_sets_fullscreen(self):
        from halloween_video_player_looper.player import VideoPlayer

        player = VideoPlayer(fullscreen=True, window_size=(720, 480), orientation=0)
        instance = mock_vlc.Instance.return_value
        media_player = instance.media_player_new.return_value
        media_player.set_fullscreen.assert_called_with(True)

    def test_stop_releases_resources(self):
        from halloween_video_player_looper.player import VideoPlayer

        player = VideoPlayer(fullscreen=False, window_size=(720, 480), orientation=0)
        player.stop()

        instance = mock_vlc.Instance.return_value
        media_player = instance.media_player_new.return_value
        media_player.stop.assert_called()
        media_player.release.assert_called()
        instance.release.assert_called()

    @patch("halloween_video_player_looper.player.time.sleep")
    def test_play_loop_plays_and_detects_end(self, mock_sleep):
        from halloween_video_player_looper.player import VideoPlayer

        player = VideoPlayer(fullscreen=False, window_size=(720, 480), orientation=0)

        instance = mock_vlc.Instance.return_value
        media_player = instance.media_player_new.return_value
        # Simulate: first call Playing, second call Ended
        media_player.get_state.side_effect = [mock_vlc.State.Playing, mock_vlc.State.Ended, mock_vlc.State.Ended]

        # Break after one loop iteration
        mock_sleep.side_effect = [None, None, KeyboardInterrupt]

        with pytest.raises(KeyboardInterrupt):
            player.play_loop(Path("/fake/video.mp4"), sleep_seconds=1)

        media_player.play.assert_called()
        media_player.set_media.assert_called()


class TestOrientationTransform:
    def test_180_degrees(self):
        from halloween_video_player_looper.player import _orientation_to_transform

        assert _orientation_to_transform(180) == "180"

    def test_0_degrees(self):
        from halloween_video_player_looper.player import _orientation_to_transform

        assert _orientation_to_transform(0) == "0"
