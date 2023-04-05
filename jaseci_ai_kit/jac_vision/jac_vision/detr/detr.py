from .model import DetrDetector
import torch
from jaseci.jsorc.live_actions import jaseci_action
import traceback
from fastapi import HTTPException
from PIL import Image
import base64
import io


@jaseci_action(act_group=["detr"], allow_remote=True)
def setup(model: str = "detr-resnet-50", device: str = None):
    global detector
    if device is None:
        _device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    else:
        _device = torch.device(device)
    detector = DetrDetector(device=_device, model=model)


@jaseci_action(act_group=["detr"], allow_remote=True)
def detect(image, b64: bool = False, threshold: float = 0.5) -> list:
    try:
        if threshold > 1 or threshold < 0:
            raise ValueError("Threshold must be between 0 and 1")
        _image = (
            Image.open(io.BytesIO(base64.b64decode(image)))
            if b64
            else Image.open(image)
        )
        return detector.detect(_image, threshold)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@jaseci_action(act_group=["detr"], allow_remote=True)
def detect_batch(images, b64: bool = False, threshold: float = 0.5) -> list:
    try:
        if threshold > 1 or threshold < 0:
            raise ValueError("Threshold must be between 0 and 1")
        _images = (
            [Image.open(io.BytesIO(base64.b64decode(image))) for image in images]
            if b64
            else [Image.open(image) for image in images]
        )
        return detector.detect_batch(_images, threshold)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@jaseci_action(act_group=["detr"], allow_remote=True)
def get_labels() -> list:
    return detector.get_labels()


if __name__ == "__main__":
    from jaseci.jsorc.remote_actions import launch_server

    launch_server(port=8000)
