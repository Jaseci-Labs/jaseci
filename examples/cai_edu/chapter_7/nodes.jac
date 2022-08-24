# Top level root node for the conversational AI
# Classify incoming request to an action-oriented flow
# or FAQ
node cai_root {
    has name = "cai_root";
    can use.text_classify;
    can categorize {
        res = use.text_classify(
            text=visitor.question,
            classes=[
                "i want to test drive",
                "I have a Model 3 reservation, how do I configure my order",
                "How do I order a tesla",
                "Can I request a Test Drive"
            ]
        );
        if (res["match_idx"] == 0):
            visitor.question_type = "va";

        else:
            visitor.question_type = "faq";
    }
}

# Parent class for conversational AI state
node cai_state {
    has name;
    can nlu {
        std.err("Node ability invoked for cai_state node: nlu");
        disengage;
    }
    can nlg {
        std.err("Node ability invoked for cai_state node: nlg");
        disengage;
    }
}

node va_state:cai_state {
    can bi_enc.train, bi_enc.infer, bi_enc.load_model, bi_enc.save_model, bi_enc.set_model_config;

    can ent_ext.entity_detection;

    # Classify the intent of the question
    can classify_intent {
        train_data = file.load_json("data/clf_train.json");
        candidates = train_data.d::keys;

        res = bi_enc.infer(
            contexts=[visitor.question],
            candidates= candidates,
            context_type="text",
            candidate_type="text"
        );

        for pred in res.list{
            # Sort result
            max_score = 0;
            max_intent = "";

            for i=0 to i < pred["candidate"].length by i+=1 {
                if (pred["score"][i] > max_score){
                    max_intent = pred["candidate"][i];
                    max_score = pred["score"][i];
                }
            }
        }

        visitor.predicted_intent = max_intent;

    }

    # Extract words of interests from the question
    can extract_entities {
       labels = [];

        train_data = file.load_json("data/flair_ner.json");

        for item in train_data {
            for ent in item["entities"] {
                ent_label = ent["entity_type"];
                if (ent_label not in labels): labels.l::append(ent_label);
            }
        }
        entity_result = ent_ext.entity_detection(
            text=visitor.question.str,
            ner_labels=labels.list
        );

        if(entity_result['entities']){
            for ent in entity_result['entities'] {
                if (ent["conf_score"] > 0.4){
                    entity_label = ent["entity_value"];
                    entity_text = ent["entity_text"];
                    if (entity_text not in visitor.extracted_entities ) {
                        visitor.extracted_entities[entity_label] = [];
                    }
                        visitor.extracted_entities[entity_label] += [entity_text];

                }

                std.out(visitor.extracted_entities);
            }
        }

        
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

node cai_va_root:va_state {
    has name = "cai_va_root";
}

node collect_info:va_state {
    has name = "collect_info";
    can gen_response {
        if ("name" in visitor.extracted_entities and
                "address" not in visitor.extracted_entities):
            visitor.response = "What is your address?";
        elif ("address" in visitor.extracted_entities and
                "name" not in visitor.extracted_entities):
            visitor.response = "What is your name?";
        else {
            visitor.response =
                "To set you up with a test drive, we will need your name and address.";
        }
    }
}

node confirmation:va_state {
    has name = "confirmation";
    can gen_response {
        visitor.response =
            "Can you confirm your name to be " + visitor.extracted_entities["name"] + " and your address as " + visitor.extracted_entities["address"] + " ?";
    }
}

node confirmed:va_state {
    has name = "confirmed";
    can gen_response {
        visitor.response = "You are all set for a Tesla test drive!";
    }
}

node canceled:va_state {
    has name = "canceled";
    can gen_response {
        visitor.response = "No worries. We look forward to hear from you in the future!";
    }
}

node faq_state:cai_state {
    has answer;
    can use.qa_classify;
    can nlu {
        answers = -[answer_transition]->.answer;
        if (answers) {
            res = use.qa_classify(
                text = visitor.question,
                classes = answers
            );
            visitor.matched_answer = res["match"];
        }
    }

    can nlg {
        visitor.response = here.answer;
    }
}