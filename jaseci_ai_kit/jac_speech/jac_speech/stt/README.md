---
title: Converting Speech in to Text
---

# **Speech2Text (`stt`)**

Module `stt` uses the `whisper` to get the transcription or translation of a give audio sequence.

1. Import [`stt`](#1-import-speech2text-stt-module-in-jac) module in jac
2. [Setup](#2-Setup)
2. [Transcribe](#3-Transcribe)
3. [Translate](#4-Translate)

# **Walk through**

## Prerequisites
1. FFmpeg
```bash
sudo apt-get install ffmpeg
```

## **1. Import Speech2Text (`stt`) module in jac**
1. For executing jaseci Open terminal and run follow command.
    ```
    jsctl -m
    ```
2.  Load whisper module in jac
    ```
    actions load module jac_speech.stt
    ```

## **2. Setup**
Use the `setup` action call to configure the model.
This step is optional.
If no `setup` is called, the default parameters are used.
### Setup Parameters
* `variant` - Model variant. Type: `str` Default: `small`. Possible values: `base`, `tiny`, `small`, `medium`, `large` (multilingual models), `small.en`, `medium.en` (Non multilingual models)

## **3. Transcribe**
There are few ways to use `stt.trascribe` action.
1. Given a audio file location, it will return the transcription of the audio.
2. Given a web url to an audio file, it will return the transcription of the audio.

All the methods uses a single action `transcribe` to get the transcription. Following are the parameters of the action.
* `audio_file` - Location to a Audio file. Type: `str` (Optional) - Works only in local mode
* `url` - Web URL to a Audio file. Type: `str` (Optional)
* `array` - Audio array. Type: `list` (Optional) (Should be sampled at 16KHz)
* `language` - Spoken Language in the Audio. Type: Type: `str` Default: `en`
* `timestamp` - Whether to return the timestamp of the transcription. Type: `bool` Default: `false`

> **Note**
> Timestamp works only in audio files that have more than 30 seconds of audio.

Return type of the action is `dict`.
example:
```json
{
    "text": "hello world. Welcome to jaseci.",
    "timestamp": [
        {
            "id": 0,
            "start": 0.0,
            "end": 1.0,
            "text": "hello world"
        },
        {
            "id": 1,
            "start": 1.0,
            "end": 2.0,
            "text": "Welcome to jaseci"
        }
    ]
}
```

```jac
walker test_transribe_file {
    can stt.transcribe;
    report stt.transcribe(audio_file="jac_speech/jac_speech/stt/tests/test.mp3");
}

walker test_transribe_url {
    can stt.transcribe;
    report stt.transcribe(url="https://www.audio-lingua.eu/IMG/mp3/les_sports.mp3", timestamp=true);
}
```

## **3. Translate**
Similar to the `stt.transcribe`, `stt.traslate` support two ways to get the english translation of a audio sequence. Currently only support `any` to `en` translation.

Following are the parameters of the action.
* `audio_file` - Location to a Audio file. Type: `str` (Optional) - Works only in local mode
* `url` - Web URL to a Audio file. Type: `str` (Optional)
* `array` - Audio array. Type: `list` (Optional) (Should be sampled at 16KHz)
* `timestamp` - Whether to return the timestamp of the transcription. Type: `bool` Default: `false`

Return type of the action is `dict`.

```jac
walker test_translate {
    can stt.translate;
    report stt.translate(url="https://www.audio-lingua.eu/IMG/mp3/les_sports.mp3");
}
```
# **References**
* [Robust Speech Recognition via Large-Scale Weak Supervision](https://cdn.openai.com/papers/whisper.pdf) by Alec Radford, Jong Wook Kim, Tao Xu, Greg Brockman, Christine McLeavey, Ilya Sutskever.
* [OpenAI Whisper](https://openai.com/blog/whisper/)
