walker test_synthesize {
    can tts.synthesize;
    report tts.synthesize("Hello world");
}

walker test_save_audio {
    can tts.synthesize;
    can tts.save_audio;
    has audio_data = tts.synthesize("Hello World, How are you? I miss you");
    report tts.save_audio(audio_data.audio_wave,"./");
}

