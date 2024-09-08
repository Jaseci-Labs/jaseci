from jaseci.jsorc.live_actions import jaseci_action
from fastapi import HTTPException
import traceback
import os
import torch
import whisper
import numpy as np
import librosa


DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


@jaseci_action(act_group=["stt"], allow_remote=True)
def setup(variant: str = "small"):
    global model, options
    model = whisper.load_model(variant, device=DEVICE)
    print(
        f"Model is {'multilingual' if model.is_multilingual else 'English-only'} "
        f"and has {sum(np.prod(p.shape) for p in model.parameters()):,} parameters."
    )


@jaseci_action(act_group=["stt"], allow_remote=True)
def transcribe(
    audio_file: str = None,
    url: str = None,
    array: list = None,
    language: str = "en",
    timestamp: bool = False,
):
    try:
        if url:
            audio_file = download_file(url)
        elif array:
            audio_file = array_to_file(array)
        if language != "en" and not model.is_multilingual:
            raise Exception(
                "Model is not multilingual. Setup with a multilingual model."
            )
        options = whisper.DecodingOptions(
            task="transcribe",
            without_timestamps=True,
            fp16=True if DEVICE == "cuda" else False,
        )
        mel, audio_length = get_mel_spectrogram(audio_file)
        if mel is None and audio_length >= 30:
            result = model.transcribe(audio_file, task="transcribe")
            transcript = result["text"]
            if timestamp:
                timestamps = [
                    {
                        "id": t["id"],
                        "start": t["start"],
                        "end": t["end"],
                        "text": t["text"],
                    }
                    for t in result["segments"]
                ]
                if url:
                    os.remove(audio_file)
                return {"text": transcript, "timestamps": timestamps}
            if url:
                os.remove(audio_file)
            return {"text": transcript}
        transcript = model.decode(mel, options).text
        if url:
            os.remove(audio_file)
        return {"text": transcript}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@jaseci_action(act_group=["stt"], allow_remote=True)
def translate(
    audio_file: str = None, url: str = None, array: list = None, timestamp: bool = False
):
    try:
        if url:
            audio_file = download_file(url)
        elif array:
            audio_file = array_to_file(array)
        if not model.is_multilingual:
            raise Exception(
                """Model is not multilingual. Setup with a multilingual model.
                Translation is not supported for English-only models."""
            )
        options = whisper.DecodingOptions(
            task="translate", fp16=True if DEVICE == "cuda" else False
        )
        mel, audio_length = get_mel_spectrogram(audio_file)
        if mel is None and audio_length >= 30:
            result = model.transcribe(audio_file, task="translate")
            transcript = result["text"]
            if timestamp:
                timestamps = [
                    {
                        "id": t["id"],
                        "start": t["start"],
                        "end": t["end"],
                        "text": t["text"],
                    }
                    for t in result["segments"]
                ]
                if url:
                    os.remove(audio_file)
                return {"text": transcript, "timestamps": timestamps}
            if url:
                os.remove(audio_file)
            return {"text": transcript}
        transcript = model.decode(mel, options).text
        if url:
            os.remove(audio_file)
        return {"text": transcript}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


def get_mel_spectrogram(audio_file: str):
    audio, _ = librosa.load(audio_file, sr=16000)
    audio_length = len(audio) / 16000
    if audio_length >= 30:
        return None, audio_length
    audio = whisper.pad_or_trim(audio.flatten())
    mel = whisper.log_mel_spectrogram(audio).to(DEVICE)
    return mel, audio_length


def array_to_file(array):
    import tempfile
    import soundfile as sf

    temp_file = tempfile.NamedTemporaryFile(delete=False)
    sf.write(temp_file.name, np.array(array), 16000)
    return temp_file.name


def download_file(url):
    import requests
    import tempfile

    temp_file = tempfile.NamedTemporaryFile(delete=False)
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        for chunk in r.iter_content(chunk_size=8192):
            temp_file.write(chunk)

    return temp_file.name


if __name__ == "__main__":
    from jaseci.jsorc.remote_actions import launch_server

    launch_server(port=8000)
