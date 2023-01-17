walker test_translate_sinhala_eng {
    can translator.translate;
    report translator.translate("හෙලෝ, කොහොමද ඔයාට?", "si_LK", "en_XX");
}

walker test_translate_eng_german {
    can translator.translate;
    report translator.translate("Hello, how are you?", "en_XX", "de_DE");
}