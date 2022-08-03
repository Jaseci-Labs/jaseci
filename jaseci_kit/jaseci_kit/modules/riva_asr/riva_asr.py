import numpy as np
import grpc
import riva_api.riva_tts_pb2 as rtts
import riva_api.riva_tts_pb2_grpc as rtts_srv
import riva_api.riva_asr_pb2_grpc as asr_srv
import riva_api.riva_asr_pb2 as asr
import riva_api.riva_audio_pb2 as ra
import base64

# NLP libraries
# import riva_api.riva_nlp_pb2_grpc as rnlp
# import riva_api.riva_nlp_pb2 as rnlp2
from jaseci.actions.live_actions import jaseci_action

server = "localhost:50051"
channel = grpc.insecure_channel(server)
stt_client = asr_srv.RivaSpeechRecognitionStub(channel)
tts_client = rtts_srv.RivaSpeechSynthesisStub(channel)


# wf = wave.open(audio_file, "rb")
# with open(audio_file, "rb") as fh:
#     data = fh.read()


@jaseci_action(act_group=["riva_asr"], allow_remote=True)
def get_stt(audio_data, frame_rate):
    audio_enc_data = base64.b64decode(audio_data)
    config = asr.RecognitionConfig(
        encoding=ra.AudioEncoding.LINEAR_PCM,
        sample_rate_hertz=frame_rate,
        language_code="en-US",
        max_alternatives=1,
        enable_automatic_punctuation=False,
        audio_channel_count=1,
    )

    request = asr.RecognizeRequest(config=config, audio=audio_enc_data)

    response = stt_client.Recognize(request)
    return response.results[0].alternatives[0].transcript


@jaseci_action(act_group=["riva_asr"], allow_remote=True)
def get_tts(text: str):
    req = rtts.SynthesizeSpeechRequest()
    req.text = text
    req.language_code = "en-US"
    req.encoding = ra.AudioEncoding.LINEAR_PCM
    req.sample_rate_hz = 22050

    resp = tts_client.Synthesize(req)

    audio_samples = np.frombuffer(resp.audio, dtype=np.float32)

    return {
        "audio_data": base64.b64encode(audio_samples),
        "frame_rate": req.sample_rate_hz,
    }


if __name__ == "__main__":
    from jaseci.actions.remote_actions import launch_server

    launch_server(port=8000)
