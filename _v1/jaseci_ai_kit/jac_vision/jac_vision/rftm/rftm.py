import torch
from PIL import Image
import torch
from jaseci.jsorc.live_actions import jaseci_action
import traceback
from fastapi import HTTPException
import base64
import io
import os
import requests
from .model import RFTM, ToTensor

RTFM_CLASSIFIER_WEIGHTS = (
    "https://huggingface.co/jaseci/rtfm/resolve/main/rtfm_classifier.pth"
)
RTFM_RESNET_101_WEIGHTS = (
    "https://huggingface.co/jaseci/rtfm/resolve/main/rtfm_resnet101.pth"
)


@jaseci_action(act_group=["rftm"], allow_remote=True)
def setup(device: str = None):
    global detector, _device
    os.makedirs("weights", exist_ok=True)
    if not os.path.exists(os.path.join("weights", "rftm_classifier.pth")):
        with open("weights/rftm_classifier.pth", "wb") as f:
            f.write(requests.get(RTFM_CLASSIFIER_WEIGHTS).content)
    if not os.path.exists(os.path.join("weights", "rftm_resnet101.pth")):
        with open("weights/rftm_resnet101.pth", "wb") as f:
            f.write(requests.get(RTFM_RESNET_101_WEIGHTS).content)

    _device = (
        torch.device("cuda" if torch.cuda.is_available() else "cpu")
        if device is None
        else torch.device(device)
    )
    detector = RFTM(device=_device)


@jaseci_action(act_group=["rftm"], allow_remote=True)
def predict(frames: list, b64: bool = False) -> float:
    try:
        if b64:
            frames = [io.BytesIO(base64.b64decode(frame)) for frame in frames]
        if len(frames) != 16:
            raise ValueError("Must have 16 frames")
        inputs = torch.Tensor(1, 3, 16, 240, 320).to()
        for num, i in enumerate(frames):
            inputs[:, :, num, :, :] = ToTensor(1)(Image.open(i))
        with torch.no_grad():
            out = detector.predict(inputs)
        return out.item()
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    from jaseci.jsorc.remote_actions import launch_server

    launch_server(port=8000)
