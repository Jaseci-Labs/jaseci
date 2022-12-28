walker test_synthesize_female {
    can vc_tts.synthesize;
    report vc_tts.synthesize(input_text = "Hello World!", speaker= "female", save_path="./");
}


walker test_synthesize_male {
    can vc_tts.synthesize;
    report vc_tts.synthesize(input_text = "Hello World!", speaker= "male", save_path="./");
}