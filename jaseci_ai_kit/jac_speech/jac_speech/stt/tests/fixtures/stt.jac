walker test_audio_to_array {
    can stt.audio_to_array;
    report stt.audio_to_array(audio_file="jac_speech/jac_speech/stt/tests/test.mp3");
}

walker test_transribe_array {
    can stt.transcribe, stt.audio_to_array;
    audio_array = stt.audio_to_array(audio_file="jac_speech/jac_speech/stt/tests/test.mp3");
    report stt.transcribe(language="en", array=audio_array);
}

walker test_transribe_file {
    can stt.transcribe;
    report stt.transcribe(language="en", audio_file="jac_speech/jac_speech/stt/tests/test.mp3");
}

walker test_transribe_url {
    can stt.transcribe;
    report stt.transcribe(language="fr", url="https://www.audio-lingua.eu/IMG/mp3/les_sports.mp3");
}

walker test_translate {
    can stt.translate;
    report stt.translate(language="fr",  url="https://www.audio-lingua.eu/IMG/mp3/les_sports.mp3");
}

