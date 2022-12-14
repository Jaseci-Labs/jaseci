walker test_translate_hindi_eng {
    can translator.translate;
    report translator.translate("नमस्ते, आप कैसे हैं?", "hi_IN", "en_XX");
}

walker test_translate_eng_german {
    can translator.translate;
    report translator.translate("Hello, how are you?", "en_XX", "de_DE");
}