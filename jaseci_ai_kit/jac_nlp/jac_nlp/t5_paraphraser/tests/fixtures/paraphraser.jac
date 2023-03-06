walker test_paraphrase {
    can t5_paraphraser.paraphrase_text;
    report t5_paraphraser.paraphrase_text(phrases=["Yiping Kang is inviting you to a scheduled Zoom meeting."]);
}
