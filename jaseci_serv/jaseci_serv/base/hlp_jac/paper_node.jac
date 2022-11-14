node cai_state {
    can bi_enc.infer;
    can tfm_ner.extract_entity;
    can use_enc.text_classify;

    has name;
    can nlu {
        ::classify_intent;
        ::extract_entities;
    }

    can classify_intent {
        intent_labels = -[intent_transition]->.edge.intent;
        predicted_intent = bi_enc.infer(
            contexts = [visitor.question],
            candidates = intent_labels,
            context_type = "text",
            candidate_type = "text"
        )[0]["predicted"]["label"];

        if (!predicted_intent) {
            predicted_intent = use_enc.text_classify(
                visitor.question,
                intent_labels
            );
        }
        visitor.wlk_ctx["intent"] = predicted_intent;
    }

    can extract_entities {
        res = tfm_ner.extract_entity(visitor.question);
        for ent in res {
            ent_type = ent["entity_value"];
            ent_text = ent["entity_text"];
            if (!(ent_type in visitor.wlk_ctx["entities"])){
                visitor.wlk_ctx["entities"][ent_type] = [];
            }
            visitor.wlk_ctx["entities"][ent_type].l::append(ent_text);
        }
    }
    can nlg {
        ...
    }
}