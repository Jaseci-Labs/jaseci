walker test_transribe_file {
    can stt.transcribe;
    report stt.transcribe(audio_file="jac_speech/jac_speech/stt/tests/test.mp3");
}

walker test_transribe_url {
    can stt.transcribe;
    report stt.transcribe(url="https://www.audio-lingua.eu/IMG/mp3/les_sports.mp3");
}

walker test_translate {
    can stt.translate;
    report stt.translate(url="https://www.audio-lingua.eu/IMG/mp3/les_sports.mp3");
}

