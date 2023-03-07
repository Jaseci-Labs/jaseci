# Jaseci Speech Package `(jac_speech)`
The `jac_speech` package contains a collection of state-of-the-art Speech models that can be used to perform various speech tasks such as speech to text, text to speech etc. following is a list of all the models available in the `jac_speech` package.

## Installation
Each module can be installed individually or all at once. To install all modules at once.
```bash
pip install jac_speech[all] # Installs all the modules present in the jac_speech package
pip install jac_speech[stt] # Installs the  stt module present in the jac_speech package
pip install jac_speech[stt,vc_tts] # Installs the stt and vc_tts module present in the jac_speech package
```

## List of Models

| Module   | Model Type     | Model Name | Docs                                | Type             | Status | Description                                            | Resources                                                                                                                                                   |
| -------- | -------------- | ---------- | ----------------------------------- | ---------------- | ------ | ------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `stt`    | Speech to Text | Whisper    | [Link](jac_speech/stt/README.md)    | No Training req. | Ready  | transcription or translation of a give audio sequence. | [Robust Speech Recognition via Large-Scale Weak Supervision](https://cdn.openai.com/papers/whisper.pdf), [OpenAI Whisper](https://openai.com/blog/whisper/) |
| `vc_tts` | Text to Speech | Coqui      | [Link](jac_speech/vc_tts/README.md) | No Training req. | Ready  | List of Amplitudes of the synthesized audio wav.       |                                                                                                                                                             |


## Usage

To load the `jac_speech.stt` package into jaseci in local environment, run the following command in the jsctl console.
```bash
jsctl > actions load module jac_speech.stt
```