# **Text to Speech with Voice Cloning (`vc_tts`)**

## **2. Synthesize audio using jaseci `vc_tts` module.**

In this section we will take an input raw text and will output the list of amplitude values of the synthesized audio. This can use to save or play the audio files using a necessary library in a preffered language.

To synthesize audios we can use the `synthesize` action in the `vc_tts` module.

**Parameters in `synthesize` action**

1. text (str) : Input text string. The accepted language is only English in this version.
2. path (str) : If you want to save the generated audio in your file system, provide the output path here.
3. rate (int) : The audio bitrate.
4. base64 (boolean) : If you want to convert the output into base64, set this value to `True`
