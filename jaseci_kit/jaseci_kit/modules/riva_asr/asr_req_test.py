# flake8: noqa
import requests
import wave
import base64
from scipy.io import wavfile

samplerate, data = wavfile.read("audio_req_file.wav")

enc_data = base64.b64encode(data).decode()
config_data = {"audio_data": enc_data, "frame_rate": samplerate}
r = requests.post("http://127.0.0.1:8000/get_stt", json=config_data)

print(f"the text is : {r.json()}")

# ======================================================================

print("Going for TTS now")

config_data = {"text": r.text[:400]}

resp = requests.post("http://127.0.0.1:8000/get_tts", json=config_data)

audio_enc_data = base64.b64decode(resp.json()["audio_data"])

out = wave.open("my_test_file.wav", "wb")
out.setnchannels(1)
out.setsampwidth(2)
out.setframerate(resp.json()["frame_rate"])
out.writeframesraw(audio_enc_data)
out.close()
