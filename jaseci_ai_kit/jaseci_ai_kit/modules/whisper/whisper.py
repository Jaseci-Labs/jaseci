from transformers import WhisperProcessor, WhisperForConditionalGeneration
import librosa
from jaseci.actions.live_actions import jaseci_action
import numpy as np
from fastapi import HTTPException
import traceback
import requests
import uuid


def setup(size: str = "tiny"):
    global model, processor
    model = WhisperForConditionalGeneration.from_pretrained(f"openai/whisper-{size}")
    processor = WhisperProcessor.from_pretrained(f"openai/whisper-{size}")


setup()


def get_array(audio_file: str = None) -> np.ndarray:  # type: ignore
    """Get numpy array from audio file"""
    audio, _ = librosa.load(audio_file, sr=16000)
    return audio


def download(url: str = None) -> str:  # type: ignore
    """Download audio file from url"""
    r = requests.get(url, allow_redirects=True)
    filename = str(uuid.uuid4()) + ".wav"
    open(filename, "wb").write(r.content)
    return filename


@jaseci_action(act_group=["whisper"], allow_remote=True)
def transcribe(language: str = "en", array: list[float] = None, audio_file: str = None, url: str = None) -> str:  # type: ignore
    try:
        global model, processor

        if array is not None:
            audio_array = np.array(array)
        elif audio_file is not None:
            audio_array = get_array(audio_file)
        elif url is not None:
            downloaded_audio_file = download(url)
            audio_array = get_array(downloaded_audio_file)
        else:
            raise ValueError("Must provide array, audio_file, or url")

        model.config.forced_decoder_ids = processor.get_decoder_prompt_ids(language=language, task="transcribe")  # type: ignore
        input_features = processor(
            audio_array, sampling_rate=16000, return_tensors="pt"
        ).input_features
        generated_ids = model.generate(input_features)  # type: ignore
        transcription = processor.batch_decode(generated_ids, skip_special_tokens=True)[
            0
        ]
        return transcription.strip()
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


@jaseci_action(act_group=["whisper"], allow_remote=True)
def translate(language: str = "fr", array: list[float] = None, audio_file: str = None, url: str = None) -> str:  # type: ignore
    try:
        global model, processor

        if array is not None:
            audio_array = np.array(array)
        elif audio_file is not None:
            audio_array = get_array(audio_file)
        elif url is not None:
            downloaded_audio_file = download(url)
            audio_array = get_array(downloaded_audio_file)
        else:
            raise ValueError("Must provide array, audio_file, or url")

        forced_decoder_ids = processor.get_decoder_prompt_ids(
            language=language, task="translate"
        )
        input_features = processor(
            audio_array, sampling_rate=16000, return_tensors="pt"
        ).input_features
        generated_ids = model.generate(input_features, forced_decoder_ids=forced_decoder_ids)  # type: ignore
        transcription = processor.batch_decode(generated_ids, skip_special_tokens=True)[
            0
        ]
        return transcription.strip()
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
