# **Text to Speech with Voice Cloning (`vc_tts`)**

## **2. Synthesize audio using jaseci `vc_tts` module.**

In this section we will take an input raw text and will output the list of amplitude values of the synthesized audio. This can use to save or play the audio files using a necessary library in a preffered language.

To synthesize audios we can use the `synthesize` action in the `vc_tts` module.

**Parameters in `synthesize` action**

1. text (str) : Input text string. The accepted language is only English in this version.
2. speaker (str) : The expected voice actor, the accepted values are here only (male,female or random)
3. path (str) : If you want to save the generated audio in your file system, provide the output path here.

Example Jac code

```
walker synthesize {
    can vc_tts.synthesize;
    report vc_tts.synthesize(input_text = "Hello World!", speaker= "male", save_path="./");
}
```

Example Output
```
{
  "success": true,
  "report": [
    {
      "save_status": true,
      "voice": "male",
      "file_path": "./audio_file_1673841425.549086.wav"
    }
  ],
  "final_node": "urn:uuid:fc151279-3cd7-4e67-8122-80ec766fc2b2",
  "yielded": false
}
```

## **3. Voice conversion using jaseci `vc_tts` module.**

1. input_text (str) : Input text string. The accepted language is only English in this version.
2. reference_audio (str) : The file path to the reference audio to clone voice. This refference audio is currenlty accepted only wav format.
3. save_path (str) :  If you want to save the generated audio in your file system, provide the output path here.

Example Jac code

```
walker clone_voice {
    can vc_tts.clone_voice;
    report vc_tts.clone_voice(input_text = "Hello World!", reference_audio= "./test_ref_audio.wav", save_path="./");
}
```

Example Output

```
{
  "success": true,
  "report": [
    {
      "save_status": true,
      "file_path": "./cloned_audio_file_1673841506.9412549.wav"
    }
  ],
  "final_node": "urn:uuid:0cb44bb9-3f63-4336-86a2-4ed9fb4c7da5",
  "yielded": false
}
```