# Parent class for conversational AI state
node cai_state {
    has name;

    can bi_enc.infer;
    can tfm_ner.extract_entity;

    # Classify the intent of the question
    can classify_intent {
        res = bi_enc.infer(
            context=[visitor.question],
            canddiates=
        )
    }

    # Extract words of interests from the question
    can extract_entities {

    }

    # Process incoming request through NLU engines
    can nlu {
        ::classify_intent;
        ::extract_entities;
    }

    # Custom business logic
    can process {

    }

    # Construct natural language response
    can nlg {

    }
}

node test_drive:cai_state {
    has name = "test_drive";
}

node collect_info:cai_state {
    has name = "collect_info";
}

node confirmation:cai_state {
    has name = "confirmation";
}

node confirmed:cai_state {
    has name = "confirmed";
}

node canceled:cai_state {
    has name = "canceled";
}
