
walker test_train{
    can fast_enc.train;
    train_data={"tell a joke": [
            "hey can you tell me a joke",
            "can you make me laugh?",
            "do you know of any jokes",
            "i want to laugh, tell me a joke please"
        ],
        "greeting": [
            "hello",
            "hi",
            "hey",
            "how's it going",
            "how are you"
        ],
        "agreement": [
            "yes let's do it",
            "I agree with you",
            "That's so true",
            "that's for sure",
            "for sure"
        ],
        "disagreement": [
            "i don't think so",
            "no",
            "nope",
            "nah",
            "no way"
        ]
    };
    report fast_enc.train(train_data=train_data,train_with_existing=false);
}

walker test_predict{
    can fast_enc.predict;
     report fast_enc.predict(sentences=["what's going on"]);
}

walker test_fast_enc_load_model{
    can fast_enc.load_model;
    report fast_enc.load_model("modeloutput");
}

walker test_fast_enc_save_model{
    can fast_enc.save_model;
    report fast_enc.save_model("modeloutput");
}