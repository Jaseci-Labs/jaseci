from .model import YolosDetector
import torch
from jaseci.actions.live_actions import jaseci_action
import traceback
from fastapi import HTTPException


def setup(device: str = None):
    global detector
    if device is None:
        _device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    else:
        _device = torch.device(device)
    detector = YolosDetector(device=_device)


setup(device=None)


@jaseci_action(act_group=["yolos"], allow_remote=True)
def detect(image, threshold: float = 0.5, b64: bool = False) -> list:
    try:
        if threshold > 1 or threshold < 0:
            raise ValueError("Threshold must be between 0 and 1")

        from PIL import Image

        if b64:
            import base64
            import io

            _image = Image.open(io.BytesIO(base64.b64decode(image)))
        else:
            _image = Image.open(image)
        return detector.detect(_image, threshold=threshold)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@jaseci_action(act_group=["yolos"], allow_remote=True)
def detect_batch(images, threshold: float = 0.5, b64: bool = False) -> list:
    try:
        if threshold > 1 or threshold < 0:
            raise ValueError("Threshold must be between 0 and 1")

        from PIL import Image

        if b64:
            import base64
            import io

            _images = [
                Image.open(io.BytesIO(base64.b64decode(image))) for image in images
            ]
        else:
            _images = [Image.open(image) for image in images]
        return detector.detect_batch(_images, threshold=threshold)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@jaseci_action(act_group=["yolos"], allow_remote=True)
def get_labels() -> list:
    return detector.get_labels()


if __name__ == "__main__":
    from jaseci.actions.remote_actions import launch_server

    launch_server(port=8000)
