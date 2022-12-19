import json
import torch
import base64
import warnings

import numpy as np

from fastapi import HTTPException
from jaseci.actions.live_actions import jaseci_action
from jaseci.actions.remote_actions import launch_server

from .action_utils import (
    rate,
    force_reload,
    save_file,
    prediction,
    load_seq2seq_model,
    load_vocorder_model,
)

warnings.filterwarnings("ignore")
warnings.warn("ignore")


seq2seqmodel = load_seq2seq_model("tacotron2_v1", force_reload)
vocorder = load_vocorder_model("waveglow", force_reload)


@jaseci_action(act_group=["tts"], allow_remote=True)
def load_seq2seqmodel(model_name: str = "tacotron2", force_reload: bool = False):
    """
    Load the sequence to sequence model. This can be use to switch beween available models.
    """
    global seq2seq_model
    try:
        seq2seq_model = load_seq2seq_model(model_name, force_reload)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return f"[Model Loaded] : {model_name}"


@jaseci_action(act_group=["tts"], allow_remote=True)
def load_vocorder(model_name: str = "waveglow", force_reload: bool = False):
    """
    Load the vocorder model. This can be use to switch between available vocordel models.
    """
    global vocorder
    try:
        vocorder = load_vocorder_model(model_name, force_reload)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return f"[Model Loaded] : {model_name}"


@jaseci_action(act_group=["tts"], allow_remote=True)
def synthesize(text: str, base64_val: bool = False, path: str = "", rate: int = rate):
    """
    Inferencing using sequence to sequence model and vocorder model.
    """
    try:
        synthesize_audio = prediction(text, seq2seqmodel, vocorder)
        if base64_val:
            json_encoded_list = json.dumps(synthesize_audio.tolist())
            output_list = base64.b64encode(json_encoded_list)
        else:
            output_list = synthesize_audio.tolist()

        if path != "":
            audio_data = np.array(output_list, dtype="float32")
            status = save_file(audio_data, path, rate)
            ret = {"audio_wave": output_list, "saving_status": status}
        else:
            output_list = synthesize_audio.tolist()
            ret = {
                "audio_wave": output_list,
            }
        return ret
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@jaseci_action(act_group=["tts"], allow_remote=True)
def save_audio(audio_data: list, path: str = "", rate: int = rate):
    """
    Saving the audio in the given file path.
    """
    try:
        audio_data = np.array(audio_data, dtype="float32")
        status = save_file(audio_data, path, rate)
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    print("Text to Speech Synthesizer up and running")
    launch_server(port=8000)
