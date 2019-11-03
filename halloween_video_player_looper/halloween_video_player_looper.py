# -*- coding: utf-8 -*-

"""
Usage:
    python halloween_video_player_looper.py -h

Notes:
    Place video files in the ./video folder.
"""

"""Main module."""
import argparse
import magic
import os
import random
import sys
from datetime import datetime
from omxplayer.player import OMXPlayer
from pprint import pprint
from time import sleep


def current_time():
    """
    Returns datetime in string format.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def file_magic(file_path):
    """
    Returns a file's file type and mime type.

    Arguments
        file_path       string
                        A file path

    Returns
        file_type       string
                        A file's file type
        mime_type       string
                        A file's mime type
    """
    file_type = magic.from_file(file_path)
    mime_type = magic.from_file(file_path, mime=True)

    return file_type, mime_type


def is_video(file_path):
    file_type, mime_type = file_magic(file_path)

    if "video" in mime_type:
        return True
    else:
        return False


def generate_video_list(video_dir=os.path.abspath("video")):
    """
    Returns a list of video file paths.

    Arguments
        video_dir       string
                        A directory path

    Returns
        video_list      list
                        A list of video file paths
    """

    if os.path.isdir(video_dir):
        video_list = []
        for root, dirs, files in os.walk(video_dir):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                if os.path.isfile(file_path):
                    if is_video(file_path) is True:
                        video_list.append(file_path)
                    else:
                        pass
                else:
                    pass

        if len(video_list) > 0:
            return video_list
        else:
            print("{} -  No video files found in {}".format(
                current_time(),
                video_dir
                ))
            print("{} - Exiting".format(current_time()))
            sys.exit()

    else:
        print("{} - Video directory does not exist {}".format(
            current_time(),
            video_dir
            )
        )
        print("{} - Create a video directory in {} and place video files in it".format(
            current_time(),
            os.path.dirname(os.path.abspath(__file__)
            )
        ))
        print("{} - Exiting".format(current_time()))
        sys.exit()


def single_video_player_looper(video_clip_path, sleep_minutes, test_mode):
    """
    Loops a single video.

    Arguments
        video_clip_path     string
                            The path of the video clip being played.

        sleep_minutes       integer or float
                            Length of time to pause between loops.

        test_mode           boolean
                            True of False. If test_mode is True, clip is not
                            played in full screen mode.
    """

    test_mode_length = "720"
    test_mode_width = "360"
    play_message = "{} - Playing {}".format(current_time(), video_clip_path)
    if test_mode is True:
        player = OMXPlayer(
            video_clip_path,
            args=[
                    "--no-osd",
                    "--loop",
                    "--win",
                    "0, 0, {0}, {1}".format(test_mode_length, test_mode_width)
                ]
        )
        play_message = "{} in test mode".format(play_message)
    else:
        player = OMXPlayer(
            video_clip_path,
            args=[
                    "--no-osd",
                    "--loop",
                    "--orientation", "180",
                    "--aspect-mode", "fill"
                ]
        )

    print(play_message)
    print("{} - {} minute(s) pause between each play".format(current_time(), sleep_minutes))

    try:
        player.pause()

        while True:
            print(play_message)
            player.play()
            sleep(player.duration())
            player.pause()
            player.set_position(0.0)
            if sleep_minutes > 0:
                if sleep_minutes < 1:
                    sleep_message = "{} seconds".format(int(60.0 * sleep_minutes))
                else:
                    sleep_message = "{} minute(s)".format(sleep_minutes)
                print("{} - Sleeping {} before starting again".format(current_time(), sleep_message))
                sleep(60 * sleep_minutes)
    except KeyboardInterrupt:
        print("{} - Exiting".format(current_time()))
        player.quit()
        sys.exit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Video looper')
    parser.add_argument("-t", "--test", help="run in test mode 720 x 360", action="store_true")
    parser.add_argument("-v", "--video", help="the video clip to run")
    parser.add_argument("-s", "--sleep", help="minutes to pause between each loop", type=float, default=0)
    parser.add_argument("-r", "--random", help="select a video at random", action="store_true")
    args = parser.parse_args()


    print("{} - Test mode:\t{}".format(current_time(), args.test))
    print("{} - Video clip:\t{}".format(current_time(), args.video))
    print("{} - Sleep time:\t{} minute(s)".format(current_time(), args.sleep))
    print("{} - Random clip:\t{}".format(current_time(), args.random))


    # sys.exit(0)

    if args.video is not None:
        if os.path.isfile(args.video):
            if is_video(args.video):
                single_video_player_looper(video_clip_path=args.video, sleep_minutes=args.sleep, test_mode=args.test)
            else:
                print("{} - Error - File is not a video file {}".format(args.video))
                print("{} - Exiting".format(current_time()))
                sys.exit()
        else:
            print("{} - Error - Video does not exist {}".format(args.video))
            print("{} - Exiting".format(current_time()))
            sys.exit()

    elif args.random is True:
        video_list = generate_video_list()
        random_video = random.choice(video_list)
        if os.path.isfile(random_video) and is_video(random_video):
            single_video_player_looper(video_clip_path=random_video, sleep_minutes=args.sleep, test_mode=args.test)
        else:
            print("{} - Error - Video does not exist {}".format(current_time(), random_video))
            print("{} - Exiting".format(current_time()))
            sys.exit()

    else:
        print("{} - No video selected. Run 'python halloween_video_player_looper.py -h' for help".format(current_time()))
        print("{} - Exiting".format(current_time()))
        sys.exit()

    """#random_video = random.choice(video_list)
    # print(random_video)
    # sys.exit()

    # try:
    #     video_dir = "video"
    #     video_list = [os.path.join(os.path.abspath(video_dir), x) for x in os.listdir(video_dir)]
    # except FileNotFoundError as e:
    #     print("{} - {} - {}".format(current_time(), type(e), str(e)))
    #     sys.exit()


    #video_clip_path = os.path.join(video_dir, "Scared Skeletons - Portrait - 28s.mp4")
    #video_clip_path = os.path.join(video_dir, "Skeleton Band - Portrait - 106s.mp4")
    #video_clip_path = os.path.join(video_dir, "Skeletons Dancing - Portrait - 71s.mp4")"""

    #single_video_player_looper(random.choice(video_list), sleep_minutes=0, test_mode=args.test)
