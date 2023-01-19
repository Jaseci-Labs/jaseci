walker test_enc_question_similarity {
    can use.question_similarity;
    report use.question_similarity("How old are you ?", "What is your age ?");
}

walker test_enc_answer_similarity {
    can use.answer_similarity;
    report use.answer_similarity("I am 30 years old", "my age is 30");
}

walker test_enc_question_classify {
    can use.question_classify;
    report use.question_classify("Share my location with Hillary's sister", ["searchplace","bookrestaurant","requestride","getdirections","getweather"]);
}

walker test_enc_answer_classify {
    can use.answer_classify;
    report use.answer_classify("Share my location with Hillary's sister", ["bookrestaurant","searchplace","requestride","getdirections","getweather"]);
}

walker test_enc_question {
    can use.enc_question;
    report use.enc_question("How old are you ?");
}

walker test_enc_answer {
    can use.enc_answer;
    report use.enc_answer("I am 30 years old");
}

walker test_enc_qa_classify{
    can use.qa_classify;
    report use.qa_classify("Share my location with Hillary's sister", ["searchplace","bookrestaurant","requestride","getdirections","getweather"]);
}

walker test_enc_qa_similarity {
    can use.qa_similarity;
    report use.qa_similarity("How old are you ?", "I am 30 years old");
}