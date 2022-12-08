walker test_audio_to_array {
    can whisper.audio_to_array;
    report whisper.audio_to_array("jaseci_ai_kit/modules/whisper/tests/test.mp3");
}

walker test_transribe_array {
    can whisper.transcribe, whisper.audio_to_array;
    audio_array = whisper.audio_to_array("jaseci_ai_kit/modules/whisper/tests/test.mp3");
    report whisper.transcribe("en", audio_array);
}

walker test_transribe_file {
    can whisper.transcribe;
    report whisper.transcribe("en", null, "jaseci_ai_kit/modules/whisper/tests/test.mp3");
}

walker test_transribe_url {
    can whisper.transcribe;
    report whisper.transcribe("fr", null, null, "https://www.audio-lingua.eu/IMG/mp3/les_sports.mp3");
}

walker test_translate {
    can whisper.translate;
    report whisper.translate("fr", null, null, "https://www.audio-lingua.eu/IMG/mp3/les_sports.mp3");
}

