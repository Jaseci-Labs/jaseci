import {
    edge::{transition, user_link}
} with "./edges.jac";

import {*} with "./globals.jac";

# Root for the entire conversational AI root
node cai_root {
    has name="cai_root";
}

# FAQ entry state
node faq_state {
    can use.question_encode, use.answer_encode;
    can vector.dot_product;
    can cl_summer.summarize;

    can seek_answer with talker entry {
        question_emb = use.question_encode(visitor.question)[0];
        max_qa_score = 0;
        for answer in -[faq_answer]-> {
            if (answer.embedding) {
                score = vector.dot_product(question_emb, answer.embedding);
                if (score > max_qa_score) {
                    max_qa_score = score;
                    visitor.destination_state = answer;
                }
            }
        }
        if (max_qa_score == 0) {
            # No FAQ is set up
            visitor.destination_state = -[faq_answer]->[0];
        }

        # For FAQ, we want the walker to take another hop
        visitor.hoping = true;
    }

    can init_answer_states with init activity {
        answers = file.load_json("data/faq_answers.json");
        answers_emb = use.answer_encode(answer=answers);
        idx = 0;
        for i in answers {
            spawn here -[faq_answer]-> node::faq_answer_state(answer=i, embedding=answers_emb[idx]);
            idx += 1;
        }
    }

    can read_url with read entry {
        summarys = cl_summer.summarize(text="none", url=visitor.source_url, sent_count=10, summarizer_type="LsaSummarizer");
        summarys_emb = use.answer_encode(answer=summarys);
        idx = 0;
        for i in summarys {
            spawn here -[faq_answer]-> node::faq_answer_state(answer=i, embedding=summarys_emb[idx]);
            idx += 1;
        }
    }

    can clean_answer_db with forget entry {
        here !-[faq_answer]-> -[faq_answer]->;
        spawn here -[faq_answer]-> node::faq_answer_state(answer="Sorry I can't handle that just yet");
    }

    can log with talker exit {
        if(here.name != "conv_root_state"){
            if(visitor.answer){
                file.append_str('result.txt', "QUESTION: " + visitor.question + " INTENT: " + visitor.predicted_intent + " CONFIDENCE: " + visitor.intent_confidence.str + " EXTRACTED ENTITIES: " + visitor.extracted_entities.str + " RESPONSE: " + visitor.answer + " STATE: " + here.name + "\n");
            }
        }
    }
}

# FAQ answer state
node faq_answer_state {
    has answer = "";
    has embedding = null;

    can speak with talker entry {
        visitor.hoping = false;
        visitor.state_for_continuing = global.conv_root_state;
        visitor.answer = here.answer;
        report {
            "name": "faq_answer",
            "response": visitor.answer
        };
    }

    can cleanup with talker entry {
        if (!visitor.hoping) {
            spawn *(global.cai_root) walker::maintainer(
                user_id = visitor.user_id,
                user_context = visitor.user_context,
                dialogue_context = visitor.dialogue_context,
                last_conv_state = visitor.state_for_continuing
            );
        }
    }
}

# Conversation state
node state {
    has anchor name;
    has cand_intents = [];
    has terms_emb = {};
    has terms_ac = {};
    has terms_data;
    has study_prompt = "";

    # AI abilities
    can use.encode, vector.cosine_sim;
    can bi_enc.get_context_emb, bi_enc.get_candidate_emb, bi_enc.infer;
    can vector.dot_product, vector.softmax;
    can ent_ext.entity_detection;
    can ent_ext.entity_detection;
    can use.answer_encode;
    can use.question_encode;
    can use.text_classify;

    # Node abilities triggered by the talker walker for convAI
    # listen -- listen to query question and analyze
    # plan -- plan the next state to move to
    # think -- process state-specific business logic
    # speak -- generate response and speak back to the user
    # cleanup -- any wrap up actions for this question
    can listen with talker entry {
        if (visitor.hoping) {
            ::classify_intent;
            ::extract_entities;
        }
    }

    can plan with talker entry {
        if (visitor.hoping) {
            visitor.destination_state = -[transition(intent_label == visitor.predicted_intent)]->[0];
        }
    }

    can think with talker entry {
        if (!visitor.hoping) {
            ::business_logic;
            # If this is a leaf node, return the root node as the node to continue from for next query
            ::collect_intents;
            if (here.cand_intents.length == 0)  {
                visitor.state_for_continuing = *(global.conv_root_state);
            } else {
                visitor.state_for_continuing = here;
            }
        }
    }

    can speak with talker entry {
        if (!visitor.hoping) {
            ::gen_response;
            report {
                "question": visitor.question,
                "name": here.name,
                "response": visitor.answer
            };
        }
    }

    can cleanup with talker entry {
        if (!visitor.hoping) {
            spawn *(global.cai_root) walker::maintainer(
                user_id = visitor.user_id,
                user_context = visitor.user_context,
                dialogue_context = visitor.dialogue_context,
                last_conv_state = visitor.state_for_continuing
            );
        }
    }

    can collect_intents {
        here.cand_intents = [];
        for i in -[transition]->.edge {
            here.cand_intents.l::append(i.intent_label);
        }
    }

    can classify_intent {
        if (visitor.hoping) {
            if (visitor.overwrite_intent != "") {
                visitor.predicted_intent = visitor.overwrite_intent;
                visitor.intent_confidence = 1;
            } else {
                if (visitor.clf_to_use == "biencoder") {
                    ::collect_intents;
                    # Use the model to perform inference
                    # returns the list of context with the suitable candidates
                    resp_data = bi_enc.infer(
                        contexts=[visitor.question],
                        candidates=here.cand_intents,
                        context_type="text",
                        candidate_type="text"
                    );

                    # Iterate through the candidate labels and their predicted scores
                    max_score = 0;
                    max_intent = "";
                    pred=resp_data[0];

                    for j=0 to j<pred["candidate"].length by j+=1 {
                        if (pred["score"][j] > max_score){
                            max_intent = pred["candidate"][j];
                            max_score = pred["score"][j];
                        }
                    }

                    visitor.predicted_intent = max_intent;
                    visitor.intent_confidence = max_score;

                } elif (visitor.clf_to_use == "use_encoder") {
                    # clf_to_use = "use_encoder"
                    dataset = file.load_json("data/clf_labels.json");

                    response = use.text_classify(visitor.question, dataset);
                    visitor.predicted_intent = response['match'];

                    max_value = null;

                    for num in response['scores']:
                        if(max_value == null or num > max_value): max_value = num;
                        
                    visitor.intent_confidence = max_value;
                } else {
                    report {"message": "missing/invalid data in clf_to_use for walker talker"};
                    disengage;
                }

                # for follow ups
                if (global.yes_label in here.cand_intents and global.no_label in here.cand_intents) {
                        # try use qa first
                        yes_prompt = "Yes";
                        no_prompt = "No";
                        q_emb = use.encode(visitor.question)[0];
                        yes_emb = use.encode(yes_prompt)[0];
                        no_emb = use.encode(no_prompt)[0];
                        yes_cos = vector.cosine_sim(q_emb, yes_emb);
                        no_cos = vector.cosine_sim(q_emb, no_emb);
                        max_score = 0;
                        pred_label = "";
                        if (yes_cos > no_cos) {
                            pred_label = global.yes_label;
                            max_score = yes_cos;
                            max_diff = (yes_cos - no_cos)/yes_cos;
                        } else {
                            pred_label = global.no_label;
                            max_score = no_cos;
                            max_diff = (no_cos - yes_cos)/no_cos;
                        }
                        if (max_score > 0.1) {
                            visitor.predicted_intent = pred_label;
                            visitor.intent_confidence = 1.0;
                        } else {
                            here.cand_intents = [];
                            for i in -[transition]->.edge {
                                if (i.intent_label not in [global.yes_label, global.no_label]){
                                    here.cand_intents.l::append(i.intent_label);
                                }
                            }
                        }
                    }
                
            }

            
        }
    }

    can extract_entities {
        if (visitor.overwrite_entity != {}) {
            visitor.extracted_entities = visitor.overwrite_entity;
        } else {
            entity_result = ent_ext.entity_detection(
                text=visitor.question, ner_labels=['item']
            );

            for ent in entity_result['entities'] {
                if (ent["conf_score"] > global.entity_confidence_threshold){
                    entity_label = ent["entity_value"];
                    entity_text = ent["entity_text"];
                    if (entity_label not in visitor.extracted_entities) {
                        visitor.extracted_entities[entity_label] = [];
                    }
                    visitor.extracted_entities[entity_label] += [entity_text];
                }
            }
        }
    }

    can business_logic {
        if (!visitor.hoping) {
            visitor.dialogue_context.dict::update(visitor.extracted_entities);
            if ("item" in visitor.extracted_entities) {
                visitor.dialogue_context["item"] = visitor.extracted_entities["item"];
            }
            // if (here.name == "hello") {
            //     visitor.dialogue_context["talking"] = true;
            // } elif (here.name == "goodbye") {
            //     visitor.dialogue_context["talking"] = false;
            // } elif (here.name == "weather") {
            //     # Call 3rd APIs to fetch weather info
            //     visitor.dialogue_context["weather"] = "sunny";
            // }
        }
    }

    can gen_response {
        if (!visitor.hoping) {
            if (here.name == "soc") {
                visitor.answer = "Hello there, Welcome to KFC!";
            } elif (here.name == "soc") {
                visitor.answer = "see ya later, have an enjoyable rest of the day!";
            } elif (here.name == "order") {
                items = " ";

                for item in visitor.dialogue_context["item"]{
                    items = items + item;
                }

                visitor.answer = "Okay so you want a " + items.str + ". Would you still like to order the item?";
            } elif (here.name == "order_confirmation") {
                visitor.answer = "Thank you for ordering with us";
            } elif (here.name == "order_denial") {
                visitor.answer = "No problem, If there anything I can help with feel free to ask";
            } elif (here.name == "eoc") {
                visitor.answer = "Bye thank you for visiting KFC, hope we can see you again next time.";
            }
        }
    }
}