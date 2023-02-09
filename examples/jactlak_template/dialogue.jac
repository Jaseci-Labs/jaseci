import {*} with "faq/faq.jac";

edge entity_transition {
    has entities;
}

edge intent_transition {
    has intent;
}

node cai_state {
    has name;
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

node dialogue_state:cai_state {
    can bi_enc.infer;
    can tfm_ner.extract_entity;
    can sbert_sim.get_sim_score;
    can ent_ext.extract_entity;
    has enc_model="bi_enc"
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

node dialogue_root;

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

node joke_state:dialogue_state {
    has name = "joke_state";
    can nlu {
        if (!visitor.wlk_ctx["intent"]): ::classify_intent;
        ::extract_entities;
    }
    can process {
        // Check entity transition
        required_entities = -[entity_transition]->.edge[0].context["entities"];
        if (vector.sort_by_key(visitor.wlk_ctx["entities"].d::keys) == vector.sort_by_key(required_entities) and !visitor.wlk_ctx["prev_state"] ) {
            visitor.wlk_ctx["next_state"] = -[entity_transition]->[0];
            visitor.wlk_ctx["prev_state"] = here;
        } else {
            visitor.wlk_ctx["respond"] = true;
        }
    }
    can nlg {
            visitor.response = "Hi, I'm JacTalk, May i know your name, please";
    }
}

node ask:dialogue_state {
    has name = "ask_question";
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
            "Hi, "+visitor.wlk_ctx["entities"]["name"][-1] + ", do you want to hear a Joke?";
    }
}

node affirm:dialogue_state {
    has name = "affirm"; 
    has joke_list=[
        "Why don't scientists trust atoms?, Because they make up everything.",
        "Where are average things manufactured?, The satisfactory.",
        "What does a nosy pepper do?, Gets jalapeño business!",
        "How does Moses make tea?, He brews."];
    can nlg {
        visitor.response = rand.choice(joke_list);
    }
}

node deny:dialogue_state {
    has name = "canceled";
    can nlg {
        visitor.response = "Bye bye, have a great day!";
    }
}

node happy:dialogue_state {
    has name = "happy";
    can nlg {
        visitor.response = "Do you want to hear another one?";
    }
}
