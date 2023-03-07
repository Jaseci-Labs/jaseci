walker test_predict{
    can sentiment.predict;

    has texts = ["I love you", "I hate you"];

    report sentiment.predict(texts);
}

