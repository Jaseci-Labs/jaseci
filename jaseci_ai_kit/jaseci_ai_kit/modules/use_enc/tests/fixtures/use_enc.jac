walker test_enc_text_similarity {
    can use.text_similarity;
    report use.text_similarity("Share my location with Hillary's sister", "getdirections");
}

walker test_enc_text_classify {
    can use.text_classify;
    report use.text_classify("Share my location with Hillary's sister", ["searchplace", "bookrestaurant",
    "requestride", "getdirections", "getweather"]);
}

walker test_enc_get_embeddings {
    can use.get_embedding;
    report use.get_embedding("Share my location with Hillary's sister");
}

walker test_enc_cos_sim_score {
    can use.cos_sim_score;
    report use.cos_sim_score([1,2,3], [1,2,4]);
}