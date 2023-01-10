walker test_synthesize {
    can tts.synthesize;
    report tts.synthesize(text="Hello World",base64_val=false);
}

walker test_save_audio {
    can tts.synthesize;
    can tts.save_audio;
    has audio_data=tts.synthesize(text="Hello World");
    report tts.save_audio(audio_data=audio_data.audio_wave, path="./");
}

walker test_load_seq2seq_model_v1{
    can tts.load_seq2seqmodel;
    report tts.load_seq2seqmodel(model_name="tacotron2_v1");
}

walker test_load_seq2seq_model_v2{
    can tts.load_seq2seqmodel;
    report tts.load_seq2seqmodel(model_name="tacotron2_v2");
}

walker test_load_vocorder_v2{
    can tts.load_vocorder;
    report tts.load_vocorder(model_name="hifigan");
}

walker test_load_vocorder_v1{
    can tts.load_vocorder;
    report tts.load_vocorder(model_name="waveglow");
}



