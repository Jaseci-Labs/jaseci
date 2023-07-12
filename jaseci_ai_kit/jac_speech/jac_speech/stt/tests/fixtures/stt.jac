walker test_transcribe_file {
    can stt.transcribe;
    report stt.transcribe(audio_file="jac_speech/stt/tests/test.mp3");
}

walker test_transcribe_url {
    can stt.transcribe;
    report stt.transcribe(url="https://audio-samples.github.io/samples/mp3/blizzard_unconditional/sample-0.mp3");
}

walker test_translate {
    can stt.translate;
    report stt.translate(url="https://audio-samples.github.io/samples/mp3/blizzard_unconditional/sample-0.mp3");
}

