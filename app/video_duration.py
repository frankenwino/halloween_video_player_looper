import subprocess
import json
import os

def video_dir():
    current_file_path = os.path.abspath(__file__)
    current_file_dir = os.path.dirname(current_file_path)
    video_dir = os.path.join(current_file_dir, "video")
    
    return video_dir
        
    
def video_duration_ffprobe(file_path):
    result = subprocess.check_output(
        f'ffprobe -v quiet -show_streams -select_streams v:0 -of json "{file_path}"',
        shell=True).decode()
    ffprobe_output_dict = json.loads(result)['streams'][0]
    duration = ffprobe_output_dict['duration']

    return duration


if __name__ == "__main__":
    video_file = "Graveyard - Landscape - 16s.mp4"
    video_file_path = os.path.join(video_dir(), video_file)
    ffprobe_duration = video_duration_ffprobe(video_file_path)
    
    print(f"ffprobe Duration:\t{ffprobe_duration} seconds")

