walker test_generate_embedding_use_enc {
    can gen_emb.generate_embedding;
    report gen_emb.generate_embedding(
        "This is a test text.",
        "use_enc"
    );
}

walker test_generate_embedding_use_qa {
    can gen_emb.generate_embedding;
    report gen_emb.generate_embedding(
        "This is a test text.",
        "use_qa"
    );
}

walker test_generate_embedding_gpt2 {
    can gen_emb.generate_embedding;
    report gen_emb.generate_embedding(
        "This is a test text.",
        "gpt2"
    );
}

walker test_generate_embedding_sbert_sim {
    can gen_emb.generate_embedding;
    report gen_emb.generate_embedding(
        "This is a test text.",
        "sbert_sim"
    );
}

walker test_generate_embedding_bi_enc {
    can gen_emb.generate_embedding;
    report gen_emb.generate_embedding(
        "This is a test text.",
        "bi_enc"
    );
}
