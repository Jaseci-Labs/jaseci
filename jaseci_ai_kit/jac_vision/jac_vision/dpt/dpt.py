from .model import DPTLarge
import torch
from jaseci.jsorc.live_actions import jaseci_action
import traceback
from fastapi import HTTPException
from PIL import Image
import base64
import io


@jaseci_action(act_group=["dpt"], allow_remote=True)
def setup(model: str = "dpt-large", device: str = None):
    global detector
    if device is None:
        _device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    else:
        _device = torch.device(device)
    detector = DPTLarge(device=_device, model=model)


@jaseci_action(act_group=["dpt"], allow_remote=True)
def estimate(image: str, b64: bool = False) -> str:
    try:
        _image = (
            Image.open(io.BytesIO(base64.b64decode(image)))
            if b64
            else Image.open(image)
        )
        depth_img = detector.estimate(_image).convert(mode="1").tobitmap()
        return base64.b64encode(depth_img).decode("utf-8")
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@jaseci_action(act_group=["dpt"], allow_remote=True)
def estimate_batch(images: list, b64: bool = False) -> list:
    try:
        _images = (
            [Image.open(io.BytesIO(base64.b64decode(image))) for image in images]
            if b64
            else [Image.open(image) for image in images]
        )
        depth_imgs = detector.estimate_batch(_images)
        return [
            base64.b64encode(depth_img.convert(mode="1").tobitmap()).decode("utf-8")
            for depth_img in depth_imgs
        ]
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    from jaseci.jsorc.remote_actions import launch_server

    launch_server(port=8000)
