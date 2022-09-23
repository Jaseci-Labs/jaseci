node dialogue_root;

node dialogue_state {
    can bi_enc.infer;
    can tfm_ner.extract_entity;

    can classify_intent {
        intent_labels = -[intent_transition]->.edge.intent;
        visitor.wlk_ctx["intent"] = bi_enc.infer(
            contexts = [visitor.question],
            candidates = intent_labels,
            context_type = "text",
            candidate_type = "text"
        )[0]["predicted"]["label"];
    }

    can extract_entities {
        // Entity extraction logic will be added a bit later on.
    }

    can init_wlk_ctx {
        new_wlk_ctx = {
            "intent": null,
            "entities": {},
            "prev_state": null,
            "next_state": null,
            "respond": false
        };
        if ("entities" in visitor.wlk_ctx) {
            // Carry over extracted entities from previous interaction
            new_wlk_ctx["entities"] = visitor.wlk_ctx["entities"];
        }
        visitor.wlk_ctx = new_wlk_ctx;
    }
    can nlu {}
    can process {
        if (visitor.wlk_ctx["prev_state"]): visitor.wlk_ctx["respond"] = true;
        else {
            visitor.wlk_ctx["next_state"] = net.root();
            visitor.wlk_ctx["prev_state"] = here;
        }
    }
    can nlg {}
}

node dialogue_root:dialogue_state {
    has name = "dialogue_root";
    can nlu {
        ::classify_intent;
    }
    can process {
        visitor.wlk_ctx["next_state"] = (-[intent_transition(intent==visitor.wlk_ctx["intent"])]->)[0];
    }
    can nlg {
        visitor.response = "Sorry I can't handle that just yet. Anything else I can help you with?";
    }
}

edge intent_transition {
    has intent;
}

graph dialogue_system {
    has anchor dialogue_root;
    spawn {
        dialogue_root = spawn node::dialogue_root;
        test_drive_state = spawn node::test_drive_state;
        td_confirmation = spawn node::td_confirmation;
        td_confirmed = spawn node::td_confirmed;
        td_canceled = spawn node::td_canceled;

        how_to_order_state = spawn node::how_to_order_state;

        dialogue_root -[intent_transition(intent="test drive")]-> test_drive_state;
        test_drive_state -[intent_transition(intent="cancel")]-> td_canceled;
        test_drive_state -[entity_transition(entities=["name", "address"])]-> td_confirmation;
        test_drive_state -[intent_transition(intent="provide name or address")]-> test_drive_state;
        td_confirmation - [intent_transition(intent="yes")]-> td_confirmed;
        td_confirmation - [intent_transition(intent="no")]-> test_drive_state;
        td_confirmation - [intent_transition(intent="cancel")]-> td_canceled;

        dialogue_root -[intent_transition(intent="order a tesla")]-> how_to_order_state;
    }
}

walker init {
    root {
        spawn here --> graph::dialogue_system;
        spawn here walker::talk;
    }
}

walker talk {
    has question;
    can bi_enc.infer;
    root {
        question = std.input("> ");
        take --> node::dialogue_root;
    }
    dialogue_root {
        intent_labels = -[intent_transition]->.edge.intent;
        predicted_intent = bi_enc.infer(
            contexts = [question],
            candidates = intent_labels,
            context_type = "text",
            candidate_type = "text"
        )[0]["predicted"]["label"];
        take -[intent_transition(intent==predicted_intent)]-> node::dialogue_state;
    }
    dialogue_state {
        std.out(here.response);
    }
}

node vehicle {
    has plate_numer;
    can get_plate_numer {
        report here.plate_number;
    }
}

node how_to_order_state:dialogue_state {
    has name = "how_to_order";
    can nlg {
        visitor.response = "You can order a Telsa through our design studio";
    }
}

node test_drive_state:dialogue_state {
    has name = "test_drive";
    can nlu {
        if (!visitor.wlk_ctx["intent"]): ::classify_intent;
        ::extract_entities;
    }
    can process {
        // Check entity transition
        required_entities = -[entity_transition]->.edge[0].context["entities"];
        if (vector.sort_by_key(visitor.wlk_ctx["entities"].d::keys) == vector.sort_by_key(required_entities)) {
            visitor.wlk_ctx["next_state"] = -[entity_transition]->[0];
            visitor.wlk_ctx["prev_state"] = here;
        } elif (visitor.wlk_ctx["prev_state"] and !visitor.wlk_ctx["prev_state"].context["name"] in ["test_drive", "td_confirmation"]){
            next_state = -[intent_transition(intent==visitor.wlk_ctx["intent"])]->;
            if (next_state.length > 0 and visitor.wlk_ctx["intent"] != "no") {
                visitor.wlk_ctx["next_state"] = next_state[0];
                visitor.wlk_ctx["prev_state"] = here;
            } else {
                visitor.wlk_ctx["respond"] = true;
            }
        } else {
            visitor.wlk_ctx["respond"] = true;
        }
    }
    can nlg {
        if ("name" in visitor.wlk_ctx["entities"] and "address" not in visitor.wlk_ctx["entities"]):
            visitor.response = "What is your address?";
        elif ("address" in visitor.wlk_ctx["entities"] and "name" not in visitor.wlk_ctx["entities"]):
            visitor.response = "What is your name?";
        else:
            visitor.response = "To set you up with a test drive, we will need your name and address.";
    }
}

node td_confirmation:dialogue_state {
    has name = "test_drive_confirmation";
    can nlu {
        if (!visitor.wlk_ctx["intent"]): ::classify_intent;
    }
    can process {
        if (visitor.wlk_ctx["prev_state"]): visitor.wlk_ctx["respond"] = true;
        else {
            visitor.wlk_ctx["next_state"] = -[intent_transition(intent==visitor.wlk_ctx["intent"])]->[0];
            visitor.wlk_ctx["prev_state"] = here;
        }
    }
    can nlg {
        visitor.response =
            "Can you confirm your name to be " + visitor.wlk_ctx["entities"]["name"][0] + " and your address as " + visitor.wlk_ctx["entities"]["address"][0] + "?";
    }
}

node td_confirmed:dialogue_state {
    has name = "test_drive_confirmed";
    can nlg {
        visitor.response = "You are all set for a Tesla test drive!";
    }
}

node td_canceled:dialogue_state {
    has name = "test_drive_canceled";
    can nlg {
        visitor.response = "No worries. We look forward to hearing from you in the future!";
    }
}

edge entity_transition {
    has entities;
}

