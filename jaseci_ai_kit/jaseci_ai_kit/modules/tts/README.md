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

**Example:**
```
walker synthesize{
    has text_input = "Hello world, I miss you so much";
    can tts.synthesize;
    result = tts.synthesize(text_input);
    report result;
}
```

**Output:**
```
    Synthesizing speeches with Tacotron2 and WaveGlow.
    "success" : True,
    "report" : [{
    "audio_wave"  :  [
        -1.3996235793456435e-05,
        -1.5296747733373195e-05,
        -1.5828527466510423e-05,
        .
        .
        .
      ]
    }
  ],
  "final_node": "urn:uuid:492ef31c-052e-477d-a003-0e8b436d8d26",
  "yielded": false
}

```
**Parameters in `synthesize` action**

1. text (str) : Input text string. The accepted language is English
2. path (str) : If you want to save the generated audio in your file system, provide the output path here.
3. rate (int) : The audio bitrate.
4. base64 (boolean) : If you want to convert the output into base64, set this value to `True`

## **3. Save generated audio into the local file system.**

You can save generated audio into local file system using the `save_audio` action from the jaseci `tts` module.

**Example:**
```
walker save_audio{
    has text_input = "Hello world!.";
    can tts.synthesize;
    can tts.save_audio;

    has result = tts.synthesize(text = text_input, base64_val= False);
    report tts.save_audio(result.audio_wave , "./");
}
```

**Output:**
```
{
  "success": true,
  "report": [
    {
      "save_status": true,
      "file_path": "./audio_file_1671440039.5007231.wav"
    }
  ],
  "final_node": "urn:uuid:e6073e75-1c25-4494-afac-eac01ee7043f",
  "yielded": false
}
```
You will see the saved audio in the given file path after completion of excuting this code.

**Parameters in `save_audio` action**

1. audio_data (list) : list of amplitude.
2. path (str) : Path to save the audio file.
3. rate (int) : audio bitrate.

## **4. Switching between available models.**

The jaseci tts module currently have two version of Tacotron2 models as sequence to sequence models and waveglow and hifigan as vocorder models. You can switch between these models using `load_seq2seqmodel` and `load_vocorder` actions acordingly. try the following example.

**Example:**
```
walker init{
    has text_input = "Hello world!.";
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

**Output:**
```
Synthesizing speeches with Tacotron2 and HIFIGAN.
{
  "success": true,
  "report": [
    {
      "save_status": true,
      "file_path": "./audio_file_1671441264.5380483.wav"
    }
  ],
  "final_node": "urn:uuid:d0993dcf-d022-4b8e-98f6-a86aa7a05652",
  "yielded": false
}
```

**Parameters in `load_seq2seqmodel` action**

1. model_name (str) : Model name, possible values : tacotron2_v1, tacotron2_v2.
2. force_reload (bool) : If true model and model is available in the cache will reuse it.

**Parameters in `load_vocorder` action**

1. model_name (str) : Model name, possible values : waveglow, hifigan.
2. force_reload (bool) : If true model and model is available in the cache will reuse it.





(video:
  file: https://user-images.githubusercontent.com/29056700/212302196-bc67e60b-a98b-426d-b5d8-f8f47a14fa75.mp4
  size: contain)



