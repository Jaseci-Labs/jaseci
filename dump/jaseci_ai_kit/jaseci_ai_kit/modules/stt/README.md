# **Speech2Text (`stt`)**

Module `stt` uses the `whisper-tiny` to get the transcription or translation of a give audio sequence.

1. Import [`stt`](#1-import-speech2text-stt-module-in-jac) module in jac
2. [Transcribe](#2-Transcribe)
3. [Translate](#3-Translate)

# **Walk through**

##Prerequisites
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
    actions load module jaseci_ai_kit.stt
    ```


## **2. Transcribe**
There are few ways to use `stt.trascribe` action.
1. Given a audio sequence array, it will return the transcription of the audio.
2. Given a audio file location, it will return the transcription of the audio.
3. Given a web url to an audio file, it will return the transcription of the audio.

All the methods uses a single action `transcribe` to get the transcription. Following are the parameters of the action.
* `language` - Spoken Language in the Audio. Type: Type: `str` Default: `en`
* `array` - Audio Array (should be sampled at 16kHz). Type: `list[float]` (Optional)
* `audio_file` - Location to a Audio file. Type: `str` (Optional) - Works only in local mode
* `url` - Web URL to a Audio file. Type: `str` (Optional)

Return type of the action is `str`.

```jac
walker transribe_array {
    can stt.transcribe, stt.audio_to_array;
    audio_array = stt.audio_to_array("test.mp3");
    report stt.transcribe("en", audio_array);
}

walker transribe_file {
    can stt.transcribe;
    report stt.transcribe("en", null, "test.mp3");
}

walker transribe_url {
    can stt.transcribe;
    report stt.transcribe("fr", null, null, "https://www.audio-lingua.eu/IMG/mp3/les_sports.mp3");
}
```

## **3. Translate**
Similar to the `stt.traslate`, `stt.traslate` support all the three ways to get the english translation of a audio sequence. Currently only support `any` to `en` translation.

Following are the parameters of the action.
* `language` - Spoken Language in the Audio. Type: Type: `str` Default: `en`
* `array` - Audio Array (should be sampled at 16kHz). Type: `list[float]` (Optional)
* `audio_file` - Location to a Audio file. Type: `str` (Optional) - Works only in local mode
* `url` - Web URL to a Audio file. Type: `str` (Optional)

Return type of the action is `str`.

```jac
walker translate {
    can stt.translate;
    report stt.translate("fr", null, null, "https://www.audio-lingua.eu/IMG/mp3/les_sports.mp3");
}
```

## **4.Support Action**
`stt` module comes with a `stt.audio_to_array` action to convert a audio file to an array. This action be used to convert a audio file to an array and then use the `stt.transcribe` action to get the transcription. This is useful when you want to get the transcription of a audio file when you are not in local mode. You can parse a base64 string of the `.wav` through `stt.audio_to_array` action and then use the returned array to get the transcription or translation.

Following are the parameters of the action.
* `audio_file` - Location to a Audio file. Type: `str` (Optional) - Works only in local mode
* `url` - Web URL to a Audio file. Type: `str` (Optional)
* `base64_str` - Base64 string of the .wav audio file. Type: `str` (Optional)

Return type of the action is `list[float]`.

```jac
walker transribe_array {
    has audio_file_base_64;
    can stt.transcribe, stt.audio_to_array;

    audio_array = stt.audio_to_array(null, null, audio_file_base_64);
    report stt.transcribe("en", audio_array);
}
```

# **References**
* [Robust Speech Recognition via Large-Scale Weak Supervision](https://cdn.openai.com/papers/whisper.pdf) by Alec Radford, Jong Wook Kim, Tao Xu, Greg Brockman, Christine McLeavey, Ilya Sutskever.
* [OpenAI Whisper](https://openai.com/blog/whisper/)