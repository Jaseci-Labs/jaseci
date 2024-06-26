"""Utility Functions for the MTLLM."""

import base64
from io import BytesIO

try:
    import cv2
except ImportError:
    cv2 = None

try:
    from PIL import Image as PILImage
except ImportError:
    PILImage = None


class Video:
    """Class to represent a video."""

    def __init__(self, file_path: str, seconds_per_frame: int = 2) -> None:
        """Initializes the Video class."""
        assert (
            cv2 is not None
        ), "Please install the required dependencies by running `pip install mtllm[video]`."
        self.file_path = file_path
        self.seconds_per_frame = seconds_per_frame

    def process(
        self,
    ) -> list:
        """Processes the video and returns a list of base64 encoded frames."""
        assert self.seconds_per_frame > 0, "Seconds per frame must be greater than 0"

        base64_frames = []

        video = cv2.VideoCapture(self.file_path)
        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = video.get(cv2.CAP_PROP_FPS)
        video_total_seconds = total_frames / fps
        assert (
            video_total_seconds > self.seconds_per_frame
        ), "Video is too short for the specified seconds per frame"
        assert (
            video_total_seconds < 4
        ), "Video is too long. Please use a video less than 4 seconds long."

        frames_to_skip = int(fps * self.seconds_per_frame)
        curr_frame = 0
        while curr_frame < total_frames - 1:
            video.set(cv2.CAP_PROP_POS_FRAMES, curr_frame)
            success, frame = video.read()
            if not success:
                break
            _, buffer = cv2.imencode(".jpg", frame)
            base64_frames.append(base64.b64encode(buffer).decode("utf-8"))
            curr_frame += frames_to_skip
        video.release()
        return base64_frames


class Image:
    """Class to represent an image."""

    def __init__(self, file_path: str) -> None:
        """Initializes the Image class."""
        assert (
            PILImage is not None
        ), "Please install the required dependencies by running `pip install mtllm[image]`."
        self.file_path = file_path

    def process(self) -> tuple[str, str]:
        """Processes the image and returns a base64 encoded image and its format."""
        image = PILImage.open(self.file_path)
        img_format = image.format
        with BytesIO() as buffer:
            image.save(buffer, format=img_format, quality=100)
            return (
                base64.b64encode(buffer.getvalue()).decode("utf-8"),
                img_format.lower(),
            )
