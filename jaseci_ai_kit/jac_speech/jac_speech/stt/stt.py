from transformers import WhisperProcessor, WhisperForConditionalGeneration
import librosa
from jaseci.actions.live_actions import jaseci_action
import numpy as np
from fastapi import HTTPException
import traceback
import requests
import uuid
import os
import base64
from typing import List

SUPPORTED_LANGUAGES = [
    "en",
    "zh",
    "de",
    "es",
    "ru",
    "ko",
    "fr",
    "ja",
    "pt",
    "tr",
    "pl",
    "ca",
    "nl",
    "ar",
    "sv",
    "it",
    "id",
    "hi",
    "fi",
    "vi",
    "iw",
    "uk",
    "el",
    "ms",
    "cs",
    "ro",
    "da",
    "hu",
    "ta",
    "no",
    "th",
    "ur",
    "hr",
    "bg",
    "lt",
    "la",
    "mi",
    "ml",
    "cy",
    "sk",
    "te",
    "fa",
    "lv",
    "bn",
    "sr",
    "az",
    "sl",
    "kn",
    "et",
    "mk",
    "br",
    "eu",
    "is",
    "hy",
    "ne",
    "mn",
    "bs",
    "kk",
    "sq",
    "sw",
    "gl",
    "mr",
    "pa",
    "si",
    "km",
    "sn",
    "yo",
    "so",
    "af",
    "oc",
    "ka",
    "be",
    "tg",
    "sd",
    "gu",
    "am",
    "yi",
    "lo",
    "uz",
    "fo",
    "ht",
    "ps",
    "tk",
    "nn",
    "mt",
    "sa",
    "lb",
    "my",
    "bo",
    "tl",
    "mg",
    "as",
    "tt",
    "haw",
    "ln",
    "ha",
    "ba",
    "jw",
    "su",
]


def setup(size: str = "tiny"):
    global model, processor
    model = WhisperForConditionalGeneration.from_pretrained(f"openai/whisper-{size}")
    processor = WhisperProcessor.from_pretrained(f"openai/whisper-{size}")


setup()


def get_array(audio_file: str = None) -> np.ndarray:
    """Get numpy array from audio file"""
    audio, _ = librosa.load(audio_file, sr=16000)
    return audio


def download(url: str = None) -> str:
    """Download audio file from url"""
    r = requests.get(url, allow_redirects=True)
    filename = str(uuid.uuid4()) + ".wav"
    open(filename, "wb").write(r.content)
    return filename


@jaseci_action(act_group=["stt"], allow_remote=True)
def transcribe(
    language: str = "en",
    array: List[float] = None,
    audio_file: str = None,
    url: str = None,
) -> str:
    try:
        global model, processor

        if language not in SUPPORTED_LANGUAGES:
            raise ValueError(f"Language {language} not supported")

        if array is not None:
            audio_array = np.array(array)
        elif audio_file is not None:
            audio_array = get_array(audio_file)
        elif url is not None:
            downloaded_audio_file = download(url)
            audio_array = get_array(downloaded_audio_file)
        else:
            raise ValueError("Must provide array, audio_file, or url")

        model.config.forced_decoder_ids = processor.get_decoder_prompt_ids(
            language=language, task="transcribe"
        )
        input_features = processor(
            audio_array, sampling_rate=16000, return_tensors="pt"
        ).input_features
        generated_ids = model.generate(input_features)
        transcription = processor.batch_decode(generated_ids, skip_special_tokens=True)[
            0
        ]
        return transcription.strip()
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


@jaseci_action(act_group=["stt"], allow_remote=True)
def translate(
    language: str = "fr",
    array: List[float] = None,
    audio_file: str = None,
    url: str = None,
) -> str:
    try:
        global model, processor

        if language not in SUPPORTED_LANGUAGES:
            raise ValueError(f"Language {language} not supported")

        if array is not None:
            audio_array = np.array(array)
        elif audio_file is not None:
            audio_array = get_array(audio_file)
        elif url is not None:
            downloaded_audio_file = download(url)
            audio_array = get_array(downloaded_audio_file)
            os.remove(downloaded_audio_file)
        else:
            raise ValueError("Must provide array, audio_file, or url")

        forced_decoder_ids = processor.get_decoder_prompt_ids(
            language=language, task="translate"
        )
        input_features = processor(
            audio_array, sampling_rate=16000, return_tensors="pt"
        ).input_features
        generated_ids = model.generate(
            input_features, forced_decoder_ids=forced_decoder_ids
        )
        transcription = processor.batch_decode(generated_ids, skip_special_tokens=True)[
            0
        ]
        return transcription.strip()
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


@jaseci_action(act_group=["stt"], allow_remote=True)
def audio_to_array(
    audio_file: str = None, url: str = None, base64_str: str = None
) -> List[float]:
    try:
        if audio_file is not None:
            audio_array = get_array(audio_file)
        elif url is not None:
            downloaded_audio_file = download(url)
            audio_array = get_array(downloaded_audio_file)
            os.remove(downloaded_audio_file)
        elif base64_str is not None:
            # save the base64 string to a file
            filename = str(uuid.uuid4()) + ".wav"
            with open(filename, "wb") as fh:
                fh.write(base64.b64decode(base64_str))
            audio_array = get_array(filename)
            os.remove(filename)
        else:
            raise ValueError("Must provide audio_file or url")
        return audio_array.tolist()
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    from jaseci.actions.remote_actions import launch_server

    launch_server(port=8000)
