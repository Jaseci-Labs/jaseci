walker test_synthesize_female {
    can tts.synthesize;
    report tts.synthesize(input_text = "Hello World!", speaker= "female", save_path="./");
}


walker test_synthesize_male {
    can tts.synthesize;
    report tts.synthesize(input_text = "Hello World!", speaker= "male", save_path="./");
}


walker test_clone_voice {
    can tts.clone_voice;
    report tts.clone_voice(input_text = "Hello World!", reference_audio= ".jac_speech/jac_speech/tts/tests/test_ref_audio.wav", save_path="./");
}
