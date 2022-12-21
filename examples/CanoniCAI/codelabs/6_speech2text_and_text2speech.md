# Making use of speech to text and speech to text modules in Jaseci

## **Speech to Text**

### **Introduction**

The process of converting spoken words into written text is called speech to text. The jaseci `stt` module can instantly transcribe the audio into a text script so that it can be shown and used as needed. Jaseci's `stt` module currently supports 99 languages.

### **Functionality of Jaseci Speech to Text Module (`stt`)**

Before work with the Jaseci `stt` module make sure to install fmmeg via `sudo apt-get install ffmpeg`. And load the jaseci `stt` module via `actions load module jaseci_ai_kit.stt`.

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

The text to speech or speech synthesizing is converting written text into audio forms. The Jaseci's `tts` module consists of two models, `encoder` and `decoder`. The encoder aka seq2seq model is similar to the Tacotron2 which converts text sequences in to mel-spectrograms. The decoder converts the audio into wav format.

### **Functionality of Jaseci Text to Speech Module (`stt`)**

Right before jump in to code lab of the Jaseci `tts` module make sure to install dependencies of sound files via `sudo apt-get install -y libsndfile1` and load the jaseci `tts` module via `actions load module jaseci_ai_kit.tts`.

**Synthesize**

From the provided raw text of input, this action can produce the amplitudes of the speech. This list of amplitudes can either be used to make audio in your preferred format , or it can be saved into a local file system as a wav file by providing the path to the preferred location.

Example
```jac
walker init{
    has text_input = "Hello world! This is a sample audio generated from the Text to speech model";
    can tts.synthesize;
    can tts.save_audio;

    has result = tts.synthesize(text = text_input, base64_val=True, path = "./");
}
```
> **Note**
>
> `tss` module allows users to switch between available models to find out what works best for their scenario. Currently Jasecis `tts` module has two version of Tacotron2(seq2seq) aka `tacotron2_v1` and `tacotron2_v2` model and two of vocoders named `waveglow` and `hifigan`.


To switch between sequence to sequence models add following lines on begining of the above code snippet,

```jac
can tts.load_seq2seqmodel;
has seq2seq_model = tts.load_seq2seqmodel("tacotron2_v2"); # tts.load_seq2seqmodel("tacotron2_v1") for version 1

```

To switch between vocoder models add following lines on begining of the above code snippet,

```jac
can tts.load_vocorder;
has vocorder = tts.load_vocorder("hifigan"); #tts.load_vocorder("waveglow") for waveglow
```
> **Note**
>
> If you don't wanna save the generated file into the current file system simply ignore giving the path variable. Also you can use `tts.save_audio` action to save the generated file into a preffered location.
>

Output
```json
"Synthesizing speeches with Tacotron2 and WaveGlow."
    {
    "success":true,
    "report" : [{"audio_wave":[
    -4.882027133135125e-05,
        -5.661428804160096e-05,
        -1.2833814253099263e-05,
        4.787599027622491e-05,
        7.041289063636214e-05,
        3.106917574768886e-05,
        -3.908021608367562e-05,
        -7.629024185007438e-05
      ],
      "saving_status": {
        "save_status": true,
        "file_path": "./audio_file_1671611719.8306742.wav"
      }
    }
  ],
  "final_node": "urn:uuid:65ce89db-39c5-4e8e-a7f7-083652412b7a",
  "yielded": false
}
```

If the code is properly executed, the created audio will be saved to the 'jac' program's current file directory.  Change the input text and play around the program.


