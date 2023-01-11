import os
import time

from TTS.api import TTS

from fastapi import HTTPException
from jaseci.actions.live_actions import jaseci_action
from jaseci.actions.remote_actions import launch_server

from .action_utils import synthesizer

model_name = "tts_models/en/vctk/vits"

speech_model = TTS(model_name)


@jaseci_action(act_group=["vc_tts"], allow_remote=True)
def synthesize(input_text: str, speaker: str, save_path: str = ""):

    speaker = speaker.lower()
    speaker_id = {"male": speech_model.speakers[3], "female": speech_model.speakers[2]}
    ret_dict = {}

    try:
        if save_path != "":
            if os.path.exists(save_path):
                file_name = "audio_file_" + str(time.time()) + ".wav"
                file_path = os.path.join(save_path, file_name)
                speech_model.tts_to_file(
                    text=input_text, speaker=speaker_id[speaker], file_path=file_path
                )
                ret_dict = {"save_status": True, "file_path": file_path}
            else:
                ret_dict = {"save_status": False}
                raise ValueError("The provided path does not exists")

        else:
            audio_wav = speech_model.tts(input_text, speaker=speaker_id[speaker])
            ret_dict = {"audio_data": audio_wav}

        return ret_dict

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@jaseci_action(act_group=["vc_tts"], allow_remote=True)
def clone_voice(input_text: str, reference_audio: str, save_path: str = "./"):

    ret_dict = {}
    try:
        if save_path != "":
            if os.path.exists(save_path):
                file_name = "cloned_audio_file_" + str(time.time()) + ".wav"
                file_path = os.path.join(save_path, file_name)
                audio_wav = synthesizer.tts(
                    text=input_text, language_name="en", speaker_wav=reference_audio
                )

                synthesizer.save_wav(wav=audio_wav, path=file_path)
                ret_dict = {"save_status": True, "file_path": file_path}
            else:
                ret_dict = {"save_status": False}
                raise ValueError("The provided path does not exists")
        else:
            audio_wav = synthesizer.tts(
                text=input_text,
                language_name="en",
                speaker_wav=reference_audio,
            )
            ret_dict = ret_dict = {"audio_data": audio_wav}
        return ret_dict

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    print("Text to Speech Synthesizer up and running")
    # clone_voice("Hello World! how are you. This is a test run. I love artificial Intelligence.", "jaseci_ai_kit/modules/vc_tts/tests/test_ref_audio.wav", "./")
    launch_server(port=8000)
