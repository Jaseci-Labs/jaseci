# Making use of speech to text and speech to text modules in Jaseci

## **Speech to Text**

### **Introduction**

The process of converting spoken words into written text is called speech to text. The jaseci `stt` module can instantly transcribe the audio into a text script so that it can be shown and used as needed. Jaseci's `stt` module currently supports 99 languages.

### **Functionality of Jaseci Speech to Text Module (`stt`)**

Before work with the Jaseci `stt` module make sure to install fmmeg via `sudo apt-get install ffmpeg`. 
Then install `pip install jac_speech[all]` which will also install the speech-to-text module which we are going to use later in this section.
And load the jaseci `stt` module via `actions load module jac_speech.stt`.

**Transcribe**

The specified audio's written transcript will be returned by `stt.transcribe` action. The audio can be provided as a mp3 file, a list of amplitude values (array), the URL to the audio(mp3) file.

Example

> **Note**
>
>Here in all the below example's we are trying with the `URL` option. if you wanna try with an mp3 file or with list of amplitudes try giving the input parameters accordingly.


```jac
walker try_transribe {
    can stt.transcribe;
     report stt.transcribe("en", null,null, "https://ia800205.us.archive.org/27/items/fifty_famous_stories_lc_librivox/fiftyfamous_00_baldwin.mp3");
}
```
Try executing the code and the compare the real audio script and the transcript return by the jaseci `stt` module. If the audio is clear and pronunciations are correct this will return 100% correct transcript.

Output:
```json
{
  "success": true,
  "report": [
    "Introduction to 50 Famous Stories Retold. This is a Librevox recording. All Librevox recordings are in the public domain. For more information or to volunteer, please visit Librevox.org. 50 Famous Stories Retold by James Baldwin. Concerning these stories. There are numerous time honored stories which have become so incorporated into the literature and thought of"
  ],
  "final_node": "urn:uuid:a5eece10-d29f-485b-893f-304a7cd63a2b",
  "yielded": false
}
```

**Translate**

In cases where the input audio is provided in any other supported language, the Jaseci's `stt.translate` action will offer the transcript in English.

Example

```jac
walker try_translate {
    can stt.translate;
    report stt.translate("fr", null, null, "https://www.audio-lingua.eu/IMG/mp3/les_sports.mp3");
}
```

Output
```json
{
  "success": true,
  "report": [
    "Hello, I'm Papal Christian and I'm going to tell you all the things I did. I did two years of calculations. I said, we did a little ... it's the coursetle ... it's the course of the multipurpose. I did after a year of foot. And after that, at that time I was going to do the gymnasticconsists of several degs. The gymnastics that consists of several degrees. And it's there, but I'm going to do it."
  ],
  "final_node": "urn:uuid:7a0fe76c-49c2-45fa-88e2-c788618949d0",
  "yielded": false
}
```

## **Text to Speech**

### **Introduction**

The text to speech or speech synthesizing is converting written text into audio forms.


### **Functionality of Jaseci Text to Speech Module (`vc_tts`)**

Right before jump in to code lab of the Jaseci `vc_tts` module make sure to install dependencies of sound files via `sudo apt-get install -y libsndfile1 espeak-ng` and load the jaseci `vc_tts` module via `actions load module jac_speech.vc_tts`.

**Synthesize**

From the provided raw text of input, this action can produce the amplitudes of the speech. You can select your preffred voice as `male` or `female`. This list of amplitudes can either be used to make audio in your preferred format , or it can be saved into a local file system as a wav file by providing the path to the preferred location.

Example
```jac
walker init{
    has text_input = "Hello world! This is a sample audio generated from the Text to speech model";
    can vc_tts.synthesize;

    has result = vc_tts.synthesize(text = text_input, speaker= "female", path = "./");
}
```

> **Note**
>
> If you don't wanna save the generated file into the current file system simply ignore giving the path variable.
>

Output
```json
{
  "success": true,
  "report": [
    {
      "save_status": true,
      "voice": "female",
      "file_path": "./audio_file_1673841425.549086.wav"
    }
  ],
  "final_node": "urn:uuid:fc151279-3cd7-4e67-8122-80ec766fc2b2",
  "yielded": false
}
```

If the code is properly executed, the created audio will be saved to the 'jac' program's current file directory.  Change the input text and play around the program.


**Clone Voice**

The voice conversion, often known as voice cloning, facility is supported by the jaseci "vc tts" module. Aka you can enter a sample voice that is at least 2.5 minutes long, and the algorithm will create the audio files by imitating the voices from the reference audio files that you have provided. Please take aware that the audio generated here will simply mimic the voice; the accent will still be American English.

Example

```
walker clone_voice {
    can vc_tts.clone_voice;
    has input_text = "
    "Hello, I'm Papal Christian and I'm going to tell you all the things I did. I did two years of calculations. I said, we did a little. it's the coursetle. it's the course of the multipurpose. I did after a year of foot. And after that, at that time I was going to do the gymnasticconsists of several degs. The gymnastics that consists of several degrees. And it's there, but I'm going to do it."

    report vc_tts.clone_voice(input_text = input_text, reference_audio= "./test_ref_audio.wav", save_path="./");
}
```

Example

```
{
  "success": true,
  "report": [
    {
      "save_status": true,
      "file_path": "./cloned_audio_file_1673841506.9412549.wav"
    }
  ],

