# Parent class for conversational AI state
node cai_state {
    has name;
    has cand_intents;

    # Collect the list of possible intents at this state
    can collect_intents {
        here.cand_intents = [];
        for i in -[intent_transition]->.edge {
            here.cand_intents.l::append(i.intent);
        }
    }

    # Classify the intent of the question
    can classify_intent {
        # NOTE: Hardcode to select the first intent from the list
        visitor.predicted_intent = here.cand_intents[0];
    }

    # Extract words of interests from the question
    can extract_entities {
        # NOTE: Hardcode to select the first intent from the list
        visitor.extracted_entities = [
            "name", "address"
        ];
    }

    can gen_response;

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
