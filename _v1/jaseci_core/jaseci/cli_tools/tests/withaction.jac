node bi_enc {
    can use.get_embedding;
}

walker init {
    root {
        std.out("loading");
        std.actload_module("jaseci_ai_kit.use_enc");
        std.out("loaded");
    }
}