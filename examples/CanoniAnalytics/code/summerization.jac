// generates the summary based on a corpse of text
walker summarization {
    can t5_sum.classify_text;
    has text;
    has anchor result;

    result = t5_sum.classify_text(text, 5, 100);

    report result;
}

walker use_encoder {
    can use.encode;
    has text;

    report use.encode(text);
}

walker init{

}