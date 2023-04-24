---
sidebar_position: 2
title: Text to Speech Module
---

# Text to Speech Module

Implementation of the `tts` module produces audio wavs from the input text sequence.

## Actions

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

## Example Jac Usage

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

For a complete example visit [here](https://github.com/Jaseci-Labs/jaseci/tree/main/jaseci_ai_kit/jac_speech/jac_speech/vc_tts)
