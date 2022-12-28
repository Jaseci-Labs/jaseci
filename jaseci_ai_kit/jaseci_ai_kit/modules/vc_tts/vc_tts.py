import os
import time

from TTS.api import TTS

from fastapi import HTTPException
from jaseci.actions.live_actions import jaseci_action
from jaseci.actions.remote_actions import launch_server

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


if __name__ == "__main__":
    print("Text to Speech Synthesizer up and running")
    launch_server(port=8000)
