walker test_generate_embedding_bi_enc {
    can gen_emb.generate_embedding;
    report gen_emb.generate_embedding(
        texts="This is a test text."
    );
}

walker test_setup {
    can gen_emb.setup;
    report gen_emb.setup(
        module_name="bi_enc"
    );
}