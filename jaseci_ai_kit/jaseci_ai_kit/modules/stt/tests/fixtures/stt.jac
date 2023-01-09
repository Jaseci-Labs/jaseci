walker test_audio_to_array {
    can stt.audio_to_array;
    report stt.audio_to_array("jaseci_ai_kit/modules/stt/tests/test.mp3");
}

walker test_transribe_array {
    can stt.transcribe, stt.audio_to_array;
    audio_array = stt.audio_to_array("jaseci_ai_kit/modules/stt/tests/test.mp3");
    report stt.transcribe("en", audio_array);
}

walker test_transribe_file {
    can stt.transcribe;
    report stt.transcribe("en", null, "jaseci_ai_kit/modules/stt/tests/test.mp3");
}

walker test_transribe_url {
    can stt.transcribe;
    report stt.transcribe("fr", null, null, "https://www.audio-lingua.eu/IMG/mp3/les_sports.mp3");
}

walker test_translate {
    can stt.translate;
    report stt.translate("fr", null, null, "https://www.audio-lingua.eu/IMG/mp3/les_sports.mp3");
}

