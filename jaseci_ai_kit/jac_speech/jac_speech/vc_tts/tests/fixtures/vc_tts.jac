walker test_synthesize_female {
    can vc_tts.synthesize;
    report vc_tts.synthesize(input_text = "Hello World!", speaker= "female", save_path="./");
}


walker test_synthesize_male {
    can vc_tts.synthesize;
    report vc_tts.synthesize(input_text = "Hello World!", speaker= "male", save_path="./");
}


walker test_clone_voice {
    can vc_tts.clone_voice;
    report vc_tts.clone_voice(input_text = "Hello World!", reference_audio= "jac_speech/vc_tts/tests/test_ref_audio.wav", save_path="./");
}
