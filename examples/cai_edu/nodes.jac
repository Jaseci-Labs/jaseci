# Parent class for conversational AI state
node cai_state {
    has name;
    has prepared_entities = {
            "name": "Tony Stark",
            "address": "10880 Malibu Point"
    };

    # Classify the intent of the question
    can classify_intent {
        # NOTE: Hardcode to select the first intent from the list
        visitor.predicted_intent = visitor.intent_override;
    }

    # Extract words of interests from the question
    can extract_entities {
        # NOTE: Hardcode to select the first intent from the list
        for ent in visitor.entity_override {
            visitor.extracted_entities[ent] = prepared_entities[ent];
        }
    }

    # Generate response
    can gen_response {
        visitor.response =
            "Sorry I can't handle that just yet! Anything else I can help you with";
    }

    # Process incoming request through NLU engines
    can nlu {
        ::classify_intent;
        ::extract_entities;
    }

    # Construct natural language response
    can nlg {
        ::gen_response;
    }
}

node collect_info:cai_state {
    has name = "collect_info";
    can gen_response {
        visitor.response =
            "To set you up for a test drive, we will need your name and address.";
    }
}

node confirmation:cai_state {
    has name = "confirmation";
    can gen_response {
        visitor.response =
            "Can you confirm your name to be " + visitor.extracted_entities["name"] + " and your address as " + visitor.extracted_entities["address"] + " ?";
    }
}

node confirmed:cai_state {
    has name = "confirmed";
    can gen_response {
        visitor.response = "You are all set for a Tesla test drive!";
    }
}

node canceled:cai_state {
    has name = "canceled";
    can gen_response {
        visitor.response = "No worries. We look forward to hear from you in the future!";
    }
}
