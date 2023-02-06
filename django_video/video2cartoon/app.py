from .white_box_cartoonizer.cartoonize import WB_Cartoonize
import skvideo.io
import numpy as np
from PIL import Image
import cv2
import os
import io
import uuid
import sys
import yaml
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.append('C:/ffmpeg/bin')

skvideo.setFFmpegPath('C:\ProgramData\Anaconda3\Lib\site-packages\skvideo\io')
with open('video2cartoon/config.yaml', 'r') as fd:
    opts = yaml.safe_load(fd)

sys.path.insert(0, './white_box_cartoonizer/')



# Init Cartoonizer and load its weights
wb_cartoonizer = WB_Cartoonize(os.path.abspath(
    "video2cartoon/white_box_cartoonizer/saved_models/"), opts['gpu'])


def cartoonize(path):
    start = time.time()

    f = str(path).rfind('\\')
    filename = str(path)[f+1:]
    print(filename)
    original_video_path = path
    

    modified_video_path = os.path.join(str(BASE_DIR) +  "\\media\\uploaded_video\\" + filename.split(".")[0] + "_modified.mp4")

    # Fetch Metadata and set frame rate
    file_metadata = skvideo.io.ffprobe(original_video_path)
    original_frame_rate = None
    if 'video' in file_metadata:
        if '@r_frame_rate' in file_metadata['video']:
            original_frame_rate = file_metadata['video']['@r_frame_rate']

    # if opts['original_frame_rate']:
    output_frame_rate = original_frame_rate
    print("***********************************")
    print(output_frame_rate)
    # else:
        # output_frame_rate = opts['output_frame_rate']

    output_frame_rate_number = int(output_frame_rate.split('/')[0])
    print(output_frame_rate_number)
    print(os.path.abspath(modified_video_path))
    
    os.system("ffmpeg -hide_banner -loglevel warning -ss 0 -i {} -filter:v scale=-1:-2 -r {} -c:a copy {}".format(
        os.path.abspath(original_video_path), output_frame_rate_number, os.path.abspath(modified_video_path)))
    

    audio_file_path = os.path.join(
        'media\\uploaded_video', filename.split(".")[0] + "_audio_modified.mp4")
    os.system("ffmpeg -hide_banner -loglevel warning -i {} -map 0:1 -vn -acodec copy -strict -2  {}".format(
        os.path.abspath(modified_video_path), os.path.abspath(audio_file_path)))


    cartoon_video_path = wb_cartoonizer.process_video(
            modified_video_path, output_frame_rate)
    

    # Add audio to the cartoonized video
    final_cartoon_video_path = os.path.join(
        'media\\uploaded_video', filename.split(".")[0] + "_cartoon_audio.mp4")
    os.system("ffmpeg -hide_banner -loglevel warning -i {} -i {} -codec copy -shortest {}".format(
        os.path.abspath(cartoon_video_path), os.path.abspath(audio_file_path), os.path.abspath(final_cartoon_video_path)))

    # Delete the videos from local disk
    os.system("rm {} {} {} {}".format(
        original_video_path, modified_video_path, audio_file_path, cartoon_video_path))

    end = time.time()
    print(f'{end-start} sec')
    
    return final_cartoon_video_path
            
    




