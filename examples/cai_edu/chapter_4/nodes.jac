# Parent class for conversational AI state
node cai_state {
    has name;
    has example_entities = {
            "name": "Tony Stark",
            "address": "10880 Malibu Point"
    };

    # Classify the intent of the question
    can classify_intent {
        # Note: a simple hardcoded "classifier"
        # To be replaced with an AI model in a later chapter
        if ("test drive" in visitor.question.str::lower):
            visitor.predicted_intent = "test drive";
        elif ("yes" in visitor.question.str::lower):
            visitor.predicted_intent = "yes";
        elif ("no" in visitor.question.str::lower):
            visitor.predicted_intent = "no";
        elif ("cancel" in visitor.question.str::lower):
            visitor.predicted_intent = "cancel";
        else:
            visitor.predicted_intent = "out of scope";
    }

    # Extract words of interests from the question
    can extract_entities {
        # Note: a simple hardcoded entity extraction model
        # To be replaced with an AI model in a later chapter
        if ("name" in visitor.question.str::lower):
            visitor.extract_entities["name"] = example_entities["name"];

        if ("address" in visitor.question.str::lower):
            visitor.extract_entities["address"] = example_entities["address"];
    }

    # Generate response
    can gen_response {
        # Default response
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

node cai_root:cai_state {
    has name = "cai_root";
}

node collect_info:cai_state {
    has name = "collect_info";
    can gen_response {
        if ("name" in visitor.extracted_entities and
                "address" not in visitor.extracted_entities):
            visitor.response = "What is your address?";
        elif ("address" in visitor.extracted_entities and
                "name" not in visitor.extracted_entities):
            visitor.response = "What is your name?";
        else:
            visitor.response =
                "To set you up with a test drive, we will need your name and address.";
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
