---
sidebar_position: 1
title: Speech to Text Module
description: Converting Speech to Text with Jaseci.
---

# Speech to Text Module

`stt` uses the `whisper-tiny` to get the transcription or translation of a give audio sequence.

## Actions

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

## Example Jac Usage:

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

For a complete example visit [here](../../../../../tutorials/jaseci_ai_kit/jac_nlp/stt)
