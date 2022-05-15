walker init {
    can bi_enc.infer;
    root {
        report bi_enc.infer(contexts = ["I like the restaurant near my house!"], candidates = ["University", "restaurant", "school", "computer"], context_type = "text", candidate_type = "text");
    }
}
