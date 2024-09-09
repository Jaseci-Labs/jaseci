walker ingest_faq {
    has kb_file;
    root: take --> node::faq_root;
    faq_root {
        kb = file.load_json(kb_file);
        for faq in kb {
            spawn here ++> node::faq_state(answer=faq["answer"]);
        }
    }
}
