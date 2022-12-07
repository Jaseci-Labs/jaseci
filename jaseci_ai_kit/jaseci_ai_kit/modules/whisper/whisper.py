from transformers import WhisperProcessor, WhisperForConditionalGeneration
import librosa
from jaseci.actions.live_actions import jaseci_action
import numpy as np


def setup(size: str = "tiny"):
    global model, processor
    model = WhisperForConditionalGeneration.from_pretrained(f"openai/whisper-{size}")
    processor = WhisperProcessor.from_pretrained(f"openai/whisper-{size}")

setup()

def get_array(audio_file: str = None) -> np.ndarray:  # type: ignore
    '''Get numpy array from audio file'''
    audio, _ = librosa.load(audio_file, sr=16000)
    return audio

def download(url: str = None) -> np.ndarray:  # type: ignore
    '''Download audio file from url'''
    pass


@jaseci_action(act_group=["whisper"], allow_remote=True)
def transcribe(audio_file:str = None, url:str = None, array:list = None, language:str = "en"):  # type: ignore
    pass

@jaseci_action(act_group=["whisper"], allow_remote=True)
def translate(audio_file:str = None, url:str = None, array:list = None, language:str = "fr"):  # type: ignore
    pass