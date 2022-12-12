# Text to Speech (tts)

Module `tts` implemented for synthesizing audio waves for the given text document. This is a example program to synthesize documents with jaseci `tts` module. We will use raw text as the input and will generate audio wav data.

1. Import `tts` module in jac
2. Synthesize audio using `tts` module.
3. Working with synthesize audio.

# **Walk through**

## **1. Import text to speech (`tts`) module in jac**

1. For executing jaseci Open terminal and run follow command.
    ```
    jsctl -m
    ```
2.  Load `tts` module in jac by command
    ```
    actions load module jaseci_ai_kit.tts
    ```
## **2. Synthesize audio using jaseci `tts` module.**

In this section we will take an input raw text and will output the list of amplitude values of the synthesized audio. This can use to save or play the audio files using a necessary library in a preffered language.

To synthesize audios we can use the `synthesize` action in the `tts` module.

```
walker synthesize{
    has text_input = "Hello world, I miss you so much";
    can tts.synthesize;
    result = tts.synthesize(text_input);
    report result;
}
```
**Parameters in `synthesize` action**

1. text (str) : Input text string. The accepted language is English
2. path (str) : If you want to save the generated audio in your file system, provide the output path here.
3. rate (int) : The audio bitrate.
4. base64 (boolean) : If you want to convert the output into base64, set this value to `True`

## **3. Save generated audio into the local file system.**

You can save generated audio into local file system using the `save_audio` action from the jaseci `tts` module.

```
walker save_audio {
    can tts.synthesize;
    can tts.save_audio;
    has audio_data = tts.synthesize("Hello World, How are you? I miss you");
    report tts.save_audio(audio_data.audio_wave,"./");
}
```

**Parameters in `save_audio` action**

1. audio_data (list) : list of amplitude.
2. path (str) : Path to save the audio file.
3. rate (int) : audio bitrate.




