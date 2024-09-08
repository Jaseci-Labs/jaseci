import os
import time
import subprocess
from pathlib import Path

from TTS.api import TTS
from TTS.utils.synthesizer import Synthesizer
from TTS.utils.manage import ModelManager


def get_models_file_path():
    return Path(__file__).parent / "models.json"


voice_cloning_model = "tts_models/multilingual/multi-dataset/your_tts"

manager = ModelManager(
    models_file=get_models_file_path(), progress_bar=True, verbose=False
)


def download_model_by_name(model_name: str):
    """
    Download the model from the checkpoint path.

    Parameters:
    -----------
    model_name: String, name of the model.

    Return:
    -----------
    model_path: String, Path to downloaded checkpoint file
    config_path: String, model configuration file path
    vocoder_path: String, vocoder model path
    vocoder_config_path: String vocoder configuration path
    """
    model_path, config_path, model_item = manager.download_model(model_name)
    if model_item["default_vocoder"] is None:
        return model_path, config_path, None, None
    vocoder_path, vocoder_config_path, _ = manager.download_model(
        model_item["default_vocoder"]
    )
    return model_path, config_path, vocoder_path, vocoder_config_path


def load_model_by_name(model_name: str, gpu: bool = False):
    """
    Load the downloaded model.

    Parameters:
    -----------
    model_name: String, name of the model.
    gpu: Boolean, if gpu is available.

    Return:
    -----------
    synthesizer: A class object of synthesizer.
    """
    model_path, config_path, vocoder_path, vocoder_config_path = download_model_by_name(
        model_name
    )

    # None values are fetch from the model
    synthesizer = Synthesizer(
        tts_checkpoint=model_path,
        tts_config_path=config_path,
        tts_speakers_file=None,
        tts_languages_file=None,
        vocoder_checkpoint=vocoder_path,
        vocoder_config=vocoder_config_path,
        encoder_checkpoint=None,
        encoder_config=None,
        use_cuda=gpu,
    )

    return synthesizer


# defining the synthesizer for voice cloning model.
synthesizer = load_model_by_name(voice_cloning_model)
