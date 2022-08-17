walker init {
    can use.enc_question, use.enc_answer;

    answers = ['I am 20 years old', 'My dog is hungry', 'My TV is broken'];
    question = "If I wanted to fix something what should I fix?";

    q_enc = use.enc_question(question);
    a_enc = use.enc_answer(answers); # can take lists or single strings

    a_scores=[];

    for i in a_enc:
        a_scores.l::append(vector.cosine_sim(q_enc, i));

    report a_scores;
}