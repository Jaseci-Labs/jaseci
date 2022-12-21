walker test_synthesize {
    can tts.synthesize;
    report tts.synthesize(text = "Hello World", base64_val= False);
}

walker test_save_audio {
    can tts.synthesize;
    can tts.save_audio;
    has audio_data = tts.synthesize(text = "Hello World! This is a test run. Wellcome to text to speech program!", base64_val= True);
    report tts.save_audio(audio_data.audio_wave,"./");
}

walker test_load_seq2seq_model_v1{
    can tts.load_seq2seqmodel;
    report tts.load_seq2seqmodel("tacotron2_v1");
}

walker test_load_seq2seq_model_v2{
    can tts.load_seq2seqmodel;
    report tts.load_seq2seqmodel("tacotron2_v2");
}

walker test_load_vocorder_v2{
    can tts.load_vocorder;
    report tts.load_vocorder("hifigan");
}

walker test_load_vocorder_v1{
    can tts.load_vocorder;
    report tts.load_vocorder("waveglow");
}

walker test_wave2mp3{
    can tts.wave2mp3;
    report tts.wave2mp3("audio_file_1671611719.8306742.wav");
}



