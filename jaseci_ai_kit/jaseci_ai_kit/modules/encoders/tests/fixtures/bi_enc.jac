walker test_bi_enc_cos_sim{
    can bi_enc.cosine_sim;
    test_data = file.load_json("cos_test_data.json");
    report bi_enc.cosine_sim(test_data['vec_a'],test_data['vec_b']);
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

walker test_bi_enc_train_config{
    can bi_enc.get_train_config;
    report bi_enc.get_train_config();
}

walker test_bi_enc_model_config{
    can bi_enc.get_model_config;
    report bi_enc.get_model_config();
}

walker test_bi_enc_train{
    can bi_enc.train;
    train_data = file.load_json("train_data.json");
    report bi_enc.train(train_data['dataset'],false,{"num_train_epochs": 2});
}

walker test_bi_enc_load_model{
    can bi_enc.load_model;
    report bi_enc.load_model("modeloutput");
}

walker test_bi_enc_save_model{
    can bi_enc.save_model;
    report bi_enc.save_model("modeloutput");
}