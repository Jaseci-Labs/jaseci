walker test_synthesize {
    can tts.synthesize;
    report tts.synthesize(text = "Hello World", seq2seq_model = "speechbrain", vocorder = "hifi_gan", base64_val= False);
}

walker test_save_audio {
    can tts.synthesize;
    can tts.save_audio;
    has audio_data = tts.synthesize(text = "Hello World! This is a test run. Wellcome to text to speech program!", base64_val= True);
    report tts.save_audio(audio_data.audio_wave,"./");
}

