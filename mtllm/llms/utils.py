'''Utility Functions for the MTLLM.'''

import base64
import os
from typing import Optional

try:
    import cv2
    from moviepy.editor import VideoFileClip
except ImportError:
    cv2 = None
    VideoFileClip = None

try:
    from PIL import Image
except ImportError:
    Image = None


class Video:
    '''Class to represent a video.'''
    def __init__(self, file_path, include_audio=False) -> None:
        assert cv2 is not None and VideoFileClip is not None, "Please install the required dependencies by running `pip install mtllm[video]`."
        self.file_path = file_path
        self.include_audio = include_audio
    
    def process_video(self, seconds_per_frame=2) -> tuple[list, Optional[str]]:
        assert seconds_per_frame > 0, "Seconds per frame must be greater than 0"

        base64Frames = []
        base_video_path, _ = os.path.splitext(self.file_path)

        video = cv2.VideoCapture(self.file_path)
        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = video.get(cv2.CAP_PROP_FPS)
        video_total_seconds = total_frames / fps
        assert video_total_seconds > seconds_per_frame, "Video is too short for the specified seconds per frame"
        assert video_total_seconds < 4, "Video is too long. Please use a video less than 4 seconds long."

        frames_to_skip = int(fps * seconds_per_frame)
        curr_frame=0
        while curr_frame < total_frames - 1:
            video.set(cv2.CAP_PROP_POS_FRAMES, curr_frame)
            success, frame = video.read()
            if not success:
                break
            _, buffer = cv2.imencode(".jpg", frame)
            base64Frames.append(base64.b64encode(buffer).decode("utf-8"))
            curr_frame += frames_to_skip
        video.release()

        audio_path = None
        if self.include_audio:
            audio_path = f"{base_video_path}.mp3"
            clip = VideoFileClip(self.file_path)
            clip.audio.write_audiofile(audio_path, bitrate="32k")
            clip.audio.close()
            clip.close()
        return base64Frames, audio_path
    
class Image:
    '''Class to represent an image.'''
    def __init__(self, file_path) -> None:
        assert Image is not None, "Please install the required dependencies by running `pip install mtllm[image]`."
        self.file_path = file_path
    
    def process_image(self) -> str:
        with open(self.file_path, "rb") as image_file:
            base64Image = base64.b64encode(image_file.read()).decode("utf-8")
        return base64Image