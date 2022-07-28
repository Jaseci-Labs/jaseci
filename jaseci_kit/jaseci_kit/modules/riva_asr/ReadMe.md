## Automated Speech Recognition with Riva ASR`(riva_asr)`

### Riva ASR`(riva_asr)` is Automated Speech Recognition module uses NVIDIA's Riva in backend. 

For this tutorial we are going to leaverage the Riva ASR for `STT` and `TTS` Use Cases
**Content Covered**
1. Intallation of NGC
2. Downloading Nvidia Riva
3. How to stand up Nvidia Riva Server
4. Walk Through for STT
5. Walk Through for TTS

### 1. Installation of NGC 
NVIDIA GPU Cloud (NGC) CLI helps you to perform many of the same operations that are available from the NGC website, such as running jobs, viewing Docker repositories and downloading AI models within your organization and team space.
1. Before Downloading NGC we need to sign up for [NGC registered Account](https://docs.nvidia.com/ngc/ngc-overview/index.html#registering-activating-ngc-account). Follow the link to register account and generate a NGC API key.
2. Follow the steps provided in [NGC](https://ngc.nvidia.com/setup/installers/cli) document to download and setup NGC for the desired environment.

### 2. Downloading Nvidia Riva
NVIDIA Riva is a GPU-accelerated SDK for building Speech AI applications that are customized for your use case and deliver real-time performance. Exectute the below command to download [NVIDIA Riva](https://docs.nvidia.com/deeplearning/riva/user-guide/docs/quick-start-guide.html).

    ngc registry resource download-version nvidia/riva/riva_quickstart:2.3.0

* Output
```
    {
    "download_end": "2022-07-28 18:18:36.783145",
    "download_start": "2022-07-28 18:18:33.779011",
    "download_time": "3s",
    "files_downloaded": 30,
    "local_path": "/home/ubuntu/riva_quickstart_v2.3.0",
    "size_downloaded": "85.86 KB",
    "status": "Completed",
    "transfer_id": "riva_quickstart_v2.3.0"
    }

```

### 3. How to stand up Nvidia Riva Server
1. To download the docker images of Nvidia Riva ASR service execute the `riva_init.sh` script inside `riva_quickstart_v2.3.0` as mentioned below
```
bash riva_init.sh
```
   * The download might take some time to complete. You can expect a similar output :
```
Logging into NGC docker registry if necessary...
Pulling required docker images if necessary...
Note: This may take some time, depending on the speed of your Internet connection.
> Pulling Riva Speech Server images.
  > Image nvcr.io/nvidia/riva/riva-speech:2.3.0-server. This may take some time...
  > Image nvcr.io/nvidia/riva/riva-speech-client:2.3.0. This may take some time... 
  > Image nvcr.io/nvidia/riva/riva-speech:2.3.0-servicemaker. This may take some time... 
.
.
.
.
Riva initialization complete. Run ./riva_start.sh to launch services.
```
2. To start up the Nvidia Riva ASR service to need to excute the `riva_start.sh` script as directed below
```
bash riva_start.sh
```
```
Starting Riva Speech Services. This may take several minutes depending on the number of models deployed.
f5a0a817b37f79a72bb0d7465a40d6f3dc5e990e8bc30c5447d59166df2640ab
Waiting for Riva server to load all models...retrying in 10 seconds
Waiting for Riva server to load all models...retrying in 10 seconds
Riva server is ready...
```
3. We also need to set up the python dependency to use riva api. Follow the below steps 
 
   * Create a `conda` environment and activate it
   * Clone the [python-client](https://github.com/nvidia-riva/python-clients) git repository
    ```
    git clone https://github.com/nvidia-riva/python-clients.git
    ```
   * Install the dependencies using following commands
    ```
    cd python-clients/
    git submodule init
    git submodule update
    pip install -r requirements.txt
    python3 setup.py bdist_wheel
    pip install --force-reinstall dist/*.whl
    ```
    * Intall the riva-api wheel inside  `riva_quickstart_v2.3.0`
    ```
    pip install riva_api-2.3.0-py3-none-any.whl
    ```
### 4. Walk Through for STT
Sample Code
```
# importing required libraries
import requests
import base64
from scipy.io import wavfile

# reading the wav audio file
samplerate, data = wavfile.read("audio_req_file.wav")

# encoding the bytedata into base64 string
enc_data = base64.b64encode(data).decode()

# creating the input data for STT api call
config_data = {"audio_data": enc_data, "frame_rate": samplerate}

# Sending request to the SST api
response = requests.post("http://127.0.0.1:8000/get_stt", json=config_data)

# Printing the response received
print(f"The text Received : {r.json()}")
```
### 5. Walk Through for TTS
Sample Code
```
# importing required libraries
import wave
import requests
import base64

# creating the input data for TTS api call
config_data = {"text": "This is Sample text for testing"}

# Sending request to the TTS api
resp = requests.post("http://127.0.0.1:8000/get_tts", json=config_data)

# decoding the base64 received response
audio_enc_data = base64.b64decode(resp.json()["audio_data"])

# Writing the received audio data in a wavfile
out = wave.open("audio_file.wav", "wb")
out.setnchannels(1)
out.setsampwidth(2)
out.setframerate(resp.json()["frame_rate"])
out.writeframesraw(audio_enc_data)
out.close()

```