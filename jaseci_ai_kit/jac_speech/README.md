---
title: Jaseci Speech Package
---

# Jaseci Speech Package `jac_speech`
The `jac_speech` package contains a collection of state-of-the-art Speech models that can be used to perform various speech tasks such as speech to text, text to speech etc. following is a list of all the models available in the `jac_speech` package.

## Speech to Text Modules

`stt` uses the `whisper-tiny` to get the transcription or translation of a give audio sequence.

### Actions

* `transcribe` : To get the transcription. Following are the parameters of the action.
  * Alternate name:
  * Input:
    * `language` - Spoken Language in the Audio. Type: Type: `str` Default: `en`
    * `array` - Audio Array (should be sampled at 16kHz). Type: `list[float]` (Optional)
    * `audio_file` - Location to a Audio file. Type: `str` (Optional) - Works only in local mode
    * `url` - Web URL to a Audio file. Type: `str` (Optional)
  * Return: Return type of the action is `str`.

* `translate` : To get the english translation of a audio sequence of different language. Following are the parameters of the action.
  * Alternate name:
  * Input:
    * `language` - Spoken Language in the Audio. Type: Type: `str` Default: `en`
    * `array` - Audio Array (should be sampled at 16kHz). Type: `list[float]` (Optional)
    * `audio_file` - Location to a Audio file. Type: `str` (Optional) - Works only in local mode
    * `url` - Web URL to a Audio file. Type: `str` (Optional)
  * Return: Return type of the action is `str`.

### Example Jac Usage:

**Example 1:**

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

**Example 2:**
```jac
walker translate {
    can stt.translate;
    report stt.translate("fr", null, null, "https://www.audio-lingua.eu/IMG/mp3/les_sports.mp3");
}
```

For a complete example visit [here](jac_speech/stt/README.md)

## Text to Speech Modules

Implementation of the `tts` module produces audio wavs from the input text sequence.

### Actions

* `synthesize`: Synthesize audio wavs for the input text sequence and will return the list of amlitude values of the audio wav. provide an option to save the audio wav in a prefered file location if the correct file path is passed as a parameter.
  * Input
    * `input_text` : (String) Input text sequence. This input text sequence will undergo with text preprocessing steps, such as expanding abrivations, converting numbers into ordinal format and removing unnessary white spaces.
    * `speaker`: (String). Choose whether you need a male or female voice.
    * `save_path` : (String) Set the path correctly if you need to save the audio in a prefered location. ignore if you don't wanna save.
  * Return
    * Dictionary

* `clone_voice`: Synthesize audio wavs for by mimicing the given reference audio clip. the input text sequence and will return the list of amlitude values of the audio wav. provide an option to save the audio wav in a prefered file location if the correct file path is passed as a parameter.
  * Input
    * `input_text` : (String) Input text sequence. This input text sequence will undergo with text preprocessing steps, such as expanding abrivations, converting numbers into ordinal format and removing unnessary white spaces.
    * `reference_audio` : (String) Path to the reference audio.
    * `save_path` : (String) Set the path correctly if you need to save the audio in a prefered location. ignore if you don't wanna save.
  * Return
    * Dictionary

### Example Jac Usage

**Example 1:**

```
walker init{
    has text_input = "Hello world!, This is a test run";
    can tts.synthesize;
    can tts.save_audio;
    can tts.load_seq2seqmodel;
    can tts.load_vocorder;

    has seq2seq = tts.load_seq2seqmodel("tacotron2_v1");
    has vocorder = tts.load_vocorder("hifigan");

    has result = tts.synthesize(text = text_input);
    report tts.save_audio(result.audio_wave , "./");
}
```

For a complete example visit [here](jac_speech/vc_tts/README.md)
