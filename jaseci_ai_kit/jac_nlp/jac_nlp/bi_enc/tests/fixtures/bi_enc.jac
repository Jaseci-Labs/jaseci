walker test_bi_enc_cos_sim{
    can bi_enc.cosine_sim;
    report bi_enc.cosine_sim([0.4659, -0.3153, 0.6579, 0.2519],[0.3732, -0.4034, 0.8592, 0.3341]);
}

walker test_bi_enc_infer{
    can bi_enc.infer;
    report bi_enc.infer(["Share my location with Hillary's sister"],["searchplace","getplacedetails","bookrestaurant","gettrafficinformation","compareplaces","sharecurrentlocation","requestride","getdirections","shareeta","getweather"],"text","text");
}

walker test_bi_enc_context_emb{
    can bi_enc.get_context_emb;
    report bi_enc.get_context_emb(["Share my location with Hillary's sister"]);
}

walker test_bi_enc_cand_emb{
    can bi_enc.get_candidate_emb;
    report bi_enc.get_candidate_emb(["sharecurrentlocation"]);
}

walker test_bi_enc_get_train_config{
    can bi_enc.get_train_config;
    report bi_enc.get_train_config();
}

walker test_bi_enc_get_model_config{
    can bi_enc.get_model_config;
    report bi_enc.get_model_config();
}

walker test_bi_enc_train{
    can bi_enc.train;
    dataset={
        "credit score question": [
            "i want to learn more about credit score",
            "can you tell me more about credit score",
            "how do improve my credit score",
            "how is my credit score calculated"
        ],
        "fair lending question": [
            "i want to learn more about redlining",
            "what can you tell me about fair lending",
            "tell me about racial gap in homeownership"
        ],
        "choosing a lender": [
            "what kind of questions should I ask my lender",
            "how to find the best lender for me",
            "help me choose a lender"
        ]
        };
    report bi_enc.train(dataset,false,{"num_train_epochs": 2});
}

walker test_bi_enc_load_model{
    can bi_enc.load_model;
    report bi_enc.load_model("modeloutput");
}

walker test_bi_enc_save_model{
    can bi_enc.save_model;
    report bi_enc.save_model("modeloutput");
}

walker test_bi_enc_set_train_config{
    can bi_enc.set_train_config;
    report bi_enc.set_train_config({"num_train_epochs": 2});
}

walker test_bi_enc_set_model_config{
    can bi_enc.set_model_config;
    report bi_enc.set_model_config({"shared": true});
}