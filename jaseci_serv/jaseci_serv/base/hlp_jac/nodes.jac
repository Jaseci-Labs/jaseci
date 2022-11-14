import {
    edge::{transition, user_link}
} with "./edges.jac";

import {*} with "./globals.jac";

# TODO: decide the best way to implement this
# node label_emebdding_cache {
#     has cache = {};
#     can get with get_emb entry {
#         if(visitor.text_key in cache) {
#             visitor.emb_value = cache[visitor.text_key];
#         }else{}
#     }
# }

# Root for the entire conversational AI root
node cai_root {
    has name="cai_root";
}

# FAQ entry state
node faq_state {
    can use.question_encode, use.answer_encode;
    can use.cos_sim_score;
    can cl_summer.summarize;

    can seek_answer with talker entry {
        # TODO: performance?
        question_emb = use.question_encode(visitor.question)[0];
        max_qa_score = 0;

        for answer in -[faq_answer]-> {
            # TODO: figure out why embedding could be a dictionary sometimes
            if (answer.embedding.type == list) {
                score = use.cos_sim_score(question_emb, answer.embedding);
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
        answers =[
            "The McDonald's app is not currently compatible with smartwatches.",
            "All the information about McDonald’s that can be shared is available on McDonald's corporate website.",
            "The McRib® has limited availability, that’s part of the reason why it’s so special. We’ll be sure to let you know when the McRib is back. In the meantime, you can try other favorites like the Big Mac®.",
            "To apply for a job at McDonald's visit the McDonalds Careers website. Navigate to Restaurant Jobs or Corporate Jobs to find available McDonald's job listings near you."
        ];
        answers_emb = use.answer_encode(answer=answers);
        idx = 0;
        # TODO: enumerate? joint iterate two list?
        for i in answers {
            spawn here -[faq_answer]-> node::faq_answer_state(answer=i, embedding=answers_emb[idx]);
            idx += 1;
        }
    }

    can read_url with read entry {
        #summarys = cl_summer.summarize(text="none", url=visitor.source_url, sent_count=10, summarizer_type="LsaSummarizer");
        summarys = cl_summer.summarize(text=visitor.source_text, url="none", sent_count=10, summarizer_type="LsaSummarizer");
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
}

# FAQ answer state
node faq_answer_state {
    has answer = "";
    has embedding = null;

    can speak with talker entry {
        visitor.hoping = false;
        # visitor.state_for_continuing = global.conv_root_state;
        visitor.answer = here.answer;
        report {
            "name": "faq_answer",
            "response": visitor.answer
        };
    }

    # can cleanup with talker entry {
    #     if (!visitor.hoping) {
    #         spawn *(global.cai_root) walker::maintainer(
    #             user_id = visitor.user_id,
    #             user_context = visitor.user_context,
    #             dialogue_context = visitor.dialogue_context,
    #             last_conv_state = visitor.state_for_continuing
    #         );
    #     }
    # }
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
    can use.encode;
    #vector.cosine_sim;
    can use.cos_sim_score;
    can bi_enc.get_context_emb, bi_enc.get_candidate_emb;
   # can vector.dot_product, vector.softmax;
    can bi_enc.dot_prod, vector.softmax;
    #can ent_ext.entity_detection;
    can tfm_ner.extract_entity;
    #can hlp.predict_poa;
    #can hlp.loan_decision;
    can use.answer_encode;
    can use.question_encode;

    # initialize term definition db from file
    # can init_terms with init entry {
    #     if (here.name == "term" or here.name == "study") {
    #         desc_list = [];
    #         terms_data = file.load_json(global.terms_json);
    #     }
    #     if (here.name == "term") {
    #         for tdata in terms_data {
    #             desc_list.l::append(tdata["term"]);
    #         }
    #         embs = use.answer_encode(desc_list);
    #         for i=0 to i<terms_data.length by i+=1 {
    #             terms_emb[terms_data[i]["term"].s::lower] = {
    #                 "emb": embs[i],
    #                 "desc": terms_data[i]["description"],
    #                 "ac": terms_data[i]["acroynm"]
    #             };
    #             if (terms_data[i]["acroynm"] != "") {
    #                 here.terms_ac[terms_data[i]["acroynm"]] = terms_data[i]["term"].s::lower;
    #             }
    #         }
    #     }
    # }

    # Node abilities triggered by the talker walker for convAI
    # listen -- listen to query question and analyze
    # plan -- plan the next state to move to
    # think -- process state-specific business logic
    # speak -- generate response and speak back to the user
    # cleanup -- any wrap up actions for this question
    can listen with talker entry {
        if (visitor.hoping) {
            ::classify_intent;
            visitor.predicted_intent = "how is my home affordability calculated";
            std.log("classified intent: " + visitor.predicted_intent);
            std.log("intent probability: " + visitor.intent_confidence.str);
            ::extract_entities;
            std.log("extracted_entities: ");
            std.log(visitor.extracted_entities);
        }
    }

    can plan with talker entry {
        if (visitor.hoping) {
            visitor.destination_state = -[transition(intent_label == visitor.predicted_intent)]->[0];
            if (visitor.intent_confidence < global.intent_confidence_threshold) {
                visitor.destination_state = *(global.conv_root_state);
             }
            #if (visitor.intent_confidence > global.intent_confidence_threshold) {
                # VA path
                # visitor.destination_state =
                #     -[transition(
                #         intent_label == visitor.predicted_intent or
                #         entity in visitor.extracted_entities)]-> node::state;
            # } else {
            #    # FAQ path
            #    visitor.destination_state = *(global.faq_state);
            # }
        }
    }

    can think with talker entry {
        if (!visitor.hoping) {
            ::business_logic;
            # If this is a leaf node, return the root node as the node to continue from for next query
            ::collect_intents;
            if (here.cand_intents.length == 0)  {
                visitor.state_for_continuing = *(global.conv_root_state);
            } elif (here.name == "term" and visitor.user_context["term_question_cnt"] < 3) {
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
            #    "state": here,
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

    can classify_intent with get_cand_intents activity {
        if (visitor.hoping) {
            if (visitor.overwrite_intent != "") {
                visitor.predicted_intent = visitor.overwrite_intent;
                visitor.intent_confidence = 1;
            } else {
                visitor.predicted_intent = "";
                # if (here.name == "term") {
                #     if (visitor.user_context["term_question_cnt"] >= 3) {
                #         yes_prompt = "Yes, let go ahead and do more";
                #         no_prompt = "No, take me to another topic";
                #         q_emb = use.question_encode(visitor.question)[0];
                #         yes_emb = use.answer_encode(yes_prompt)[0];
                #         no_emb = use.answer_encode(no_prompt)[0];
                #         yes_cos = vector.cosine_sim(q_emb, yes_emb);
                #         no_cos = vector.cosine_sim(q_emb, no_emb);
                #         if (yes_cos > no_cos) {
                #             visitor.predicted_intent = global.yes_label;
                #         } else {
                #             visitor.predicted_intent = global.no_label;
                #         }
                #         visitor.intent_confidence = 1.0;
                #     }
                if (here.name == "study") {
                    prompts = {
                        "repeat1": "I can repeat the first topical concept definition to you.",
                        "repeat2": "I can repeat the second topical concept definition to you.",
                        "repeat3": "I can repeat the third topical concept definition to you.",
                        "repeat4": "I can repeat the fourth topical concept definition to you.",
                        "another": "I will give you another new definition concept or term.",
                        "leaving": "We can change topic and leave this conversation."
                        #"test_me": "I will test you."
                    };
                    max_score = 0;
                    max_prompt = "";
                    q_emb = use.question_encode(visitor.question)[0];
                    for kv_pair in prompts.dict::items {
                        a_emb = use.answer_encode(kv_pair[1])[0];
                        #score = vector.cosine_sim(q_emb, a_emb);
                        score = use.cos_sim_score(q_emb, a_emb);
                        if (score > max_score) {
                            max_score = score;
                            max_prompt = kv_pair[0];
                        }
                    }
                    if (max_prompt == "leaving") {
                        visitor.predicted_intent = "leaving_label";
                        # reset term_question_cnt
                        visitor.user_context["term_question_cnt"] = 0;
                    } else {
                        visitor.predicted_intent = "stay_label";
                    }
                    here.study_prompt = max_prompt;
                    visitor.intent_confidence = 1.0;
                } else {
                    ::collect_intents;
                    # special case for followup
                    if (global.yes_label in here.cand_intents and global.no_label in here.cand_intents) {
                        # try use qa first
                        yes_prompt = "Yes";
                        no_prompt = "No";
                        q_emb = use.encode(visitor.question)[0];
                        yes_emb = use.encode(yes_prompt)[0];
                        no_emb = use.encode(no_prompt)[0];
                        #yes_cos = vector.cosine_sim(q_emb, yes_emb);
                        yes_cos = use.cos_sim_score(q_emb, yes_emb);
                        #no_cos = vector.cosine_sim(q_emb, no_emb);
                        no_cos = use.cos_sim_score(q_emb, no_emb);
                        std.log('&&&&&&&&&&&');
                        std.log(yes_cos);
                        std.log(no_cos);
                        std.log('&&&&&&&&&&&');
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
                    if (visitor.predicted_intent == "") {
                        question_emb = bi_enc.get_context_emb(contexts=[visitor.question])[0];
                        dot_product_array = [];
                        for i in here.cand_intents {
                            intent_emb = bi_enc.get_candidate_emb(candidates=[i])[0];
                            dot_product = bi_enc.dot_prod(question_emb, intent_emb);
                            dot_product_array.l::append(dot_product);
                        }
                        # Apply a softmax
                        softmax_out = vector.softmax(dot_product_array);
                        idx = 0;
                        max_score = 0.0;
                        for j in softmax_out {
                            if (j > max_score) {
                                max_score = j;
                                visitor.predicted_intent = here.cand_intents[idx];
                            }
                            idx += 1;
                        }
                        visitor.intent_confidence = max_score;
                    }
                }
            }
        }
    }

    can extract_entities {
        if (visitor.overwrite_entity != {}) {
            visitor.extracted_entities = visitor.overwrite_entity;
        } else {
            entity_result = tfm_ner.extract_entity(
                text=visitor.question
            );
            std.log(entity_result);
            for ent in entity_result {
                if (ent["score"] > global.entity_confidence_threshold){
                    entity_label = ent["entity_type"];
                    entity_label = "LOC";
                    entity_text = ent["entity_value"];
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
            if ("LOC" in visitor.extracted_entities) {
                visitor.dialogue_context["location"] = visitor.extracted_entities["LOC"][0];
            }
            if (here.name == "prob_of_approval") {
                # temp_loan_profile = visitor.user_context["loan_profile"];

                # for key in temp_loan_profile.dict::keys:
                #     if(temp_loan_profile[key].type == dict){
                #         temp_loan_profile[key] = "";
                #     }

                #std.log(temp_loan_profile);
                #pred_approval = hlp.predict_poa(temp_loan_profile);
                pred_approval = hlp.predict_poa(visitor.user_context["loan_profile"]);
                visitor.dialogue_context["predicted_loan_approval"] = pred_approval[0];
            } elif (here.name == "saving_advice") {
                visitor.dialogue_context["avg_spend"] =
                    visitor.user_context["db"]["average_spending"];
            } elif (here.name == "study") {
                # TODO: switch this if we wish to move study under term again
                #if (visitor.predicted_intent == global.yes_label) {
                if (visitor.predicted_intent == global.study_label) {
                    rand_idx = rand.integer(0, here.terms_data.length-1);
                    select_term = here.terms_data[rand_idx];
                    if ("study_count" not in visitor.user_context) {
                        visitor.user_context["study_count"] = 0;
                    }
                    visitor.user_context["study_count"] += 1;
                    visitor.answer = "Great! Let's talk about " + select_term["term"] + ". " + select_term["description"];
                    visitor.user_context["studied_terms"] = [select_term];
                } elif (here.study_prompt == "another") {
                    if ("study_count" not in visitor.user_context) {
                        visitor.user_context["study_count"] = 0;
                    }
                    visitor.user_context["study_count"] += 1;
                    rand_idx = rand.integer(0, here.terms_data.length-1);
                    select_term = here.terms_data[rand_idx];
                    #select_term = rand.choice(terms_data);
                    prefix = [
                        "Cool! I think you would be interested to learn about ",
                        "Here is another one, ",
                        "This one trips people up, "
                    ];
                    pre = prefix[rand.integer(0, prefix.length-1)];
                    visitor.answer = pre + select_term["term"] + ". " + select_term["description"];
                    visitor.user_context["studied_terms"].l::append(select_term);
                } else {
                    if(here.study_prompt == "repeat1") {
                        repeat_idx = 0;
                    } elif(here.study_prompt == "repeat2") {
                        repeat_idx = 1;
                    } elif(here.study_prompt == "repeat3") {
                        repeat_idx = 2;
                    } elif(here.study_prompt == "repeat4") {
                        repeat_idx = 3;
                    } else {
                        repeat_idx = -1;
                    }
                    if (repeat_idx >= visitor.user_context["studied_terms"].length) {
                        # THIS SHOULDN"T Happen. Basically this is for when things fail
                        if ("study_count" not in visitor.user_context) {
                            visitor.user_context["study_count"] = 0;
                        }
                        visitor.user_context["study_count"] += 1;
                        rand_idx = rand.integer(0, here.terms_data.length-1);
                        select_term = here.terms_data[rand_idx];
                        visitor.answer = "Alright. Here it is -- " + select_term["term"] + ". " + select_term["description"];
                        visitor.user_context["studied_terms"].l::append(select_term);
                    } else {
                        repeated_term = visitor.user_context["studied_terms"][repeat_idx];
                        visitor.answer = "Of course! That one was about " + repeated_term["term"] + ". Specifically, " + repeated_term["description"];
                    }
                }
            } elif (here.name == "term") {
                if ("term_question_cnt" not in visitor.user_context) {
                    visitor.user_context["term_question_cnt"] = 0;
                }
                visitor.user_context["term_question_cnt"] += 1;
                # Can fin term ner
                term_entities = ent_ext.entity_detection(
                    text=visitor.question,
                    ner_labels=["Fin_Corp"]
                )["entities"];
                for ent in term_entities {
                    entity_label = ent["entity_value"];
                    entity_text = ent["entity_text"];
                    if (entity_label not in visitor.extracted_entities) {
                        visitor.extracted_entities[entity_label] = [];
                    }
                    visitor.extracted_entities[entity_label] += [entity_text];
                }
                std.log("======Entities==========");
                std.log(visitor.extracted_entities);
                std.log("======Entities==========");

                # concatenante extracted terms
                if ("Fin_Corp" in visitor.extracted_entities) {
                    terms = visitor.extracted_entities["Fin_Corp"];
                    term_name = "";
                    for term in terms {
                        if (term_name == "") {
                            term_name = term;
                        } else {
                            term_name += " " + term;
                        }
                    }
                    # first check if it is an acryonm or exact match
                    if (term_name in here.terms_ac) {
                        matched_term = here.terms_emb[here.terms_ac[term_name]];
                        matched_term_name = here.terms_ac[term_name];
                    } elif (term_name.s::lower in here.terms_emb) {
                        matched_term = here.terms_emb[term_name.s::lower];
                        matched_term_name = term_name;
                    } else {
                        in_emb = use.answer_encode(term_name)[0];
                        max_score = 0.0;
                        matched_term = null;
                        matched_term_name = "";
                        for t in here.terms_emb.keys {
                            other_emb = here.terms_emb[t]["emb"];
                            #cos_score = vector.cosine_sim(in_emb, other_emb);
                            cos_score = use.cos_sim_score(in_emb, other_emb);
                            if (cos_score > max_score) {
                                max_score = cos_score;
                                matched_term = here.terms_emb[t];
                                matched_term_name = t;
                            }
                        }
                    }
                    prefix = [
                        "It sounds like you are asking about ",
                        "No worries I have the info on ",
                        "Here is the meaning of "
                    ];
                    pre = prefix[rand.integer(0, prefix.length-1)];
                    visitor.answer = pre + matched_term_name + ". " + matched_term["desc"];
                    visitor.resp_payload = matched_term;
                }
            }
        }
    }

    can gen_response {
        # TODO: load these response from a file
        # TODO: move the user context update to business logic
        if (!visitor.hoping) {
            if (here.name == "conv_root_state"){
                visitor.answer = "Sorry, I can't handle that just yet. But I am constantly learning new skills! At the moment, I have knowledge about your loan approval likelihood and home affordability. Anything else I can help you with?";

            } elif (here.name == "home_price_inquiry") {
                if ("location" in visitor.dialogue_context) {
                    ::get_housing_price;
                    draw = rand.integer(1, 3);
                    if (draw == 0) {
                        visitor.answer = "The average price of a home in " +
                        visitor.dialogue_context["location"] + " is " + visitor.dialogue_context["price"];
                    } elif (draw == 1) {
                        visitor.answer = "I got you. If you are looking at places in " + visitor.dialogue_context["location"] + ", you are probably looking at prices around " +  visitor.dialogue_context["price"];
                    } elif (draw == 2) {
                        visitor.answer = "After analyzing the housing market in " + visitor.dialogue_context["location"] + ", I can tell you that the houses there are averaging around " + visitor.dialogue_context["price"];
                    } elif (draw == 3) {
                        visitor.answer = visitor.dialogue_context["location"]  + " is a great area to look at and we are talking about roughly " + visitor.dialogue_context["price"] + " on average.";
                    }
                } else {
                    visitor.answer = "I can absolutely help you with home price information. " +
                    "Is there a specific area you have in mind?";
                }
            } elif (here.name == "prob_of_approval") {
                if (visitor.dialogue_context["predicted_loan_approval"] == 1.0) {
                    // draw = rand.integer(0, 2);
                    std.log(visitor.user_context);
                    afford_min = visitor.user_context["loan_profile"]["affordabilityRange"]["minAffordability"];
                    afford_max = visitor.user_context["loan_profile"]["affordabilityRange"]["maxAffordability"];
                    // if (draw == 0) {
                    //     visitor.answer = "Good news! Based on our smart AI model, I think you have a decent chance to get approved for a home between $" + afford_min.str + " and $" + afford_max.str + ". With that being said, there are other ways to increase your chance even further, such as decrease your credit card debit. Do you want to learn more?";
                    // } elif (draw == 1) {
                    //     visitor.answer = "Don't worry. After analyzing your financial history, I think you are in a good place to get approved for a loan for a home between $" + afford_min.str + " and $" + afford_max.str + ". Adjusting your credit card balance can further help you. Want to give it a try?";
                    // } elif (draw == 2) {
                    //     visitor.answer = "If I am right in my prediction (which I usually am), you should have no major issue securing a loan approval for a home between $" + afford_min.str + " and $" + afford_max.str + ". On the other hand, there are some actionables you can take to make it even more safe. Want to take a look at, say, your credit card balance?";
                    // }
                    visitor.answer = "After analyzing your financial history, and based on my calculations, I think you are in a good place to get approved for a loan for a home between $" + afford_min.str +" and $" + afford_max.str + ". There are further steps to take that could help increase this amount, would you like to learn more?";
                } else {
                    visitor.answer = "Based on our estimates, we feel you may have some difficulty getting approved for a loan. Would you like to learn about steps you can take to improve your chances in the future?";
                }
            } elif (here.name == "prob_of_approval_confirmation") {
                visitor.answer = "Great. Our Improvement Plan page already has some recommendations on that let me take you there now!";
            } elif (here.name == "prob_of_approval_denial") {
                visitor.answer = "No problem. Always here to help if you need me!";
            } elif (here.name == "bank_acct_connect") {
                if (visitor.dialogue_context['loan_profile']["firstName"]) {
                    name = visitor.dialogue_context['loan_profile']["firstName"];
                    visitor.answer = "Hey "+ name +", looks like you've been exploring our site! Would you like me to help you connect your banking information? Also, did you know that you can earn cash rewards towards your down payment for simply connecting your bank account information? Pretty neat!";
                } else {
                    visitor.answer = "Hey, looks like you've been exploring our site! Would you like me to help you connect your banking information? Also, did you know that you can earn cash rewards towards your down payment for simply connecting your bank account information? Pretty neat!";
                }
            } elif (here.name == "bank_acct_connect_confirmation") {
                visitor.answer = "Great! Here's where you can connect any of your bank accounts!";
            } elif (here.name == "bank_acct_connect_denial") {
                visitor.answer = "No problem, let me know if you need any assistance!";
            } elif (here.name == "loan_approval_strategy") {
                visitor.answer = "Based on my cash flow analysis, you could apply an addition $300 " +
                "per month towards the balance without affecting your quality of life. " +
                "Would you like to proceed?";
            } elif (here.name == "loan_approval_strategy_confirmation") {
                visitor.answer = "Ok, I have your 4-month payment plan at $458 per month for $1832. " +
                "I even gave you a little cushion if needed.";
            } elif(here.name == "improvement_plan"){
                visitor.answer = "Sure! Let me take you there and you can not only see more detail about your home of interest, but also see how you could improve things like your credit score!";
            } elif (here.name == "chance_of_approval_improvement") {
                if("cred_score_num" in visitor.user_context["loan_profile"]){
                    credit_score = visitor.user_context["loan_profile"]["cred_score_num"];
                    visitor.answer = "Thats a great question! After analyzing your data and crunching the numbers, it looks like your credit score of " + credit_score.str + " is the main factor that is affecting your chances of getting approved for a loan. Would you like to learn steps you can take to improve your credit score?";
                } else {
                    visitor.answer = "Thats a great question! After analyzing your data and crunching the numbers, it looks like your credit score is the main factor that is affecting your chances of getting approved for a loan. Would you like to learn steps you can take to improve your credit score?";
                }
            } elif(here.name == "chance_of_approval_improvement_confirmation"){
                visitor.answer = "Ok great! let me take you to the improvement plan page and you can simulate how to improve your credit score! Here are some helpful links that also provide more ways to improve your credit score! https://www.investopedia.com/how-to-improve-your-credit-score-4590097  https://www.nerdwallet.com/article/finance/raise-credit-score";
            } elif(here.name == "chance_of_approval_improvement_denial"){
                visitor.answer = "No problem, let me know if you need anything else!";
            } elif (here.name == "page_size_improvement"){
                visitor.answer = "Sure thing! I have just enlarged the page view for you. Let me know if this works.";
            } elif (here.name == "saving_advice") {
                if (visitor.user_context["history"]["spending_reduction_rec"]) {
                    if (visitor.user_context["history"]["down_payment_programs"]) {
                        visitor.answer = "The last time we chatted, I saved our top down payment assitance programs " +
                        "in your profile. Please check them out when you get chance!";
                    } else {
                        visitor.answer = "Here are my best recommendations on down payment assistance programs " +
                        "that will help you most based on your profile. " +
                        "Should I add them to your profile for when you are ready to connect to a lender?";
                    }
                } else {
                    visitor.answer = "Absolutely! I noticed you've been spending an average of " +
                    visitor.dialogue_context["avg_spend"]["restaurant"] +
                    " per month on restaurants. Any chance you would be interested in purchasing " +
                    "a monthly subscription to a service such as Blue Apron to lower this cost? " +
                    "I estimate that you could save an average of $500 per month if you did!";
                }
            } elif (here.name == "saving_advice_confirmation") {
                if (visitor.user_context["history"]["spending_reduction_rec"]) {
                    visitor.user_context["history"]["down_payment_programs"] = true;
                    visitor.answer = "Great! The program information are in your profile now! " +
                    "Anything else you need help with at the moment?";
                } else {
                    visitor.answer = "I got this! I just sent you an email to sign up for Blue Apron. " +
                    "Let me know how this goes, and I will recommend other ways to put you in better position to " +
                    "buy the home of you dreams.";
                    visitor.user_context["history"]["spending_reduction_rec"] = true;
                }
            } elif (here.name == "saving_advice_denial") {
                visitor.user_context["history"]["spending_reduction_rec"] = true;
                visitor.answer = "No problem. I will have the information ready for whenever you are ready to revisit it. " +
                "Anything else I can help you with at the moment?";
            } elif (here.name == "loan_approval_denial") {
                visitor.answer = "No problem. I will have the information ready for whenever you are ready to revisit it. " +
                "Anything else I can help you with at the moment?";
            } elif (here.name == "tell_a_joke") {
                jokes = [
                    "What do you call a woman who sets her mortgage documents on fire? Bernadette",
                    "I thought people would flock to my bank if I offered 0% mortgages. But there was literally no interest.",
                    "What is a mortgage officer's favorite Mexican food? Refied beans",
                    "What do you call a platypus wearing a tuxedo that takes out a loan to buy stock in a mortgage company? Interesting.",
                    "What do you call an actor who finished paying-off his house loan? Mortgage Freeman"
                ];
                i = rand.integer(0, jokes.length-1);
                visitor.answer = jokes[i];
            } elif (here.name == "home_interests") {
                prefix = [
                    "I was able to find",
                    "This house is",
                    "Let me share with you",
                    "Enjoy"
                ];
                suffix = [
                    "If I were you, I'd get this one. But I'm AI so I have to live in your computer.",
                    "Given your finances you can totally snag this one up. If only bots like me can go on vacation.",
                    "I've picked this just for you based on your profile. I love geting to know you.",
                    "This house would be perfect for you ... (and me)"
                ];
                mids = [
                    "a gorgeous 4,200SF custom home on 3 beautiful & natural acres. Feel the vacation-like rural tranquility.",
                    "a Stately, Custom built home rests on a gorgeous 1.5 Acre wooded lot in Glennborough.",
                    "a rare opportunity to own this 5-year new, spectacular & fully customized traditional style home.",
                    "a stunning bird's eye view of Ann Arbor from this exclusive 10th & 11th floor penthouse in the One North Main building."
                ];
                pre = prefix[rand.integer(0, prefix.length-1)];
                suf = suffix[rand.integer(0, suffix.length-1)];
                mid = mids[rand.integer(0, mids.length-1)];
                visitor.answer = pre + " " + mid + " " + suf;
            } elif (here.name == "greeting") {
                visitor.answer = "I'm doing well, how about you?";
            } elif (here.name == "intro") {
                visitor.answer = "Hey! That's exactly what I am here fore. I will guide you through this so no worries at all! What can I help to start with?";
            } elif (here.name == "my_data") {
                visitor.answer = "QUERY MY DATA";
            # } elif (here.name == "term") {
            #     if (visitor.user_context["term_question_cnt"] == 3) {
            #         visitor.answer += " If you'd like I can coach you through some other important topics. Are you in?";
            #     }
            } elif (here.name == "conv_root_state"){
                visitor.user_context["term_question_cnt"] = 0;
                visitor.answer = "Okay sounds good. What else can I help with?";
                #visitor.answer = "Is there anything else I could help you with?";
            } elif (here.name == "fin_summary"){
                visitor.answer = "The Financial Summary provides a high level snapshot of your current assets and gross monthly debts. It also allows you to edit the amounts originally pulled from your plaid profile, if you feel they are not fully represented";
            } elif (here.name == "taxes_calc") {
                visitor.answer = "Great question! Your taxes were calculated by looking at your Federal, State and Local taxes, if applicable. Would you like me to look up what your current local taxes are?";
            } elif(here.name == "taxes_calc_confirmation") {
                visitor.answer = "Sure thing. Here are some additional information on tax calculation: https://www.usa.gov/state-taxes";
            } elif(here.name == "taxes_calc_denial") {
                visitor.answer = "No worries, feel free to reach out if you need assistance!";
            } elif (here.name == "home_close_docs") {
                visitor.answer = "I know it can seem overwhelming, but I'm here to help! Typically you would need to submit the following: W2 Forms for the past two years, recent bank statement, copy of your ID and copy of your Social Security Card. Does this help?";
            } elif (here.name == "home_close_docs_confirmation") {
                visitor.answer = "Glad I can help! Let me know if you need further assistance";
            } elif (here.name == "home_close_docs_denial") {
                visitor.answer = "Let me see how can help you further! Here's a link that may help you understand what documents are needed: https://www.creditkarma.com/home-loans/i/home-loan-documents";
            } elif (here.name == "home_afdb_calc") {
                visitor.answer = "To calculate how much house you can afford, we take into account a few primary items, such as your household income, monthly debts (for example, car loan and student loan payments) and the amount of available savings for a down payment. As a home buyer, you'll want to have a certain level of comfort in understanding your monthly mortgage payments. Can I navigate you to our Help Simulator that can allow you to test how you can increase your affordability?";
            } elif (here.name == "home_afdb_inc") {
                std.log("in home_afdb_inc response block");
                visitor.answer = "I'm glad you asked! Typically, there are a few steps you can take to increase your affordability such as the following: Increase your down payment, Increasing credit score, Increase in your monthly income. Are you interested in learning more about potential programs you may qualify for with regards to down payment assistance?";
            } elif (here.name == "home_afdb_inc_confirmation"){
                visitor.answer = "Using our downpayment resources we will display programs below that you are qualified for.";
            } elif (here.name == "home_afdb_inc_denial"){
                visitor.answer = "No worries, always here to help!";
            } elif (here.name == "home_afdb_calc_confirmation") {
                visitor.answer = "Let me navigate you to the improvement plan page.";
            } elif (here.name == "home_afdb_calc_denial") {
                visitor.answer = "No problem, always here to help!";
            } elif (here.name == "home_afdb_var"){
                visitor.answer = "Great question! The reason your affordability varies from state to state is because each state has its own unique attributes for things such as taxes and cost for homeowners insurance. My algorithm takes these factors into account, and runs calculations based on your current financial profile. Would you like to learn more? ";
            } elif (here.name == "home_afdb_var_confirmation"){
                visitor.answer = "Ok awesome! Check out these links to learn more!: https://www.nerdwallet.com/article/taxes/state-income-tax-rates, https://www.kiplinger.com/kiplinger-tools/taxes/t055-s001-kiplinger-tax-map/index.php";
            } elif (here.name == "home_afdb_var_denial"){
                visitor.answer = "Ok sounds good! Let me know if you need any further assistance";
            } elif (here.name == "docs_to_upload"){
                visitor.answer = "Sure thing! I can see you've already uploaded your W2 Forms for the past two years, great work! You still need to upload recent bank statements and copies of your Driver's License and Social Security card. Can I help you with your Finances?";
            } elif (here.name == "docs_to_upload_confirmation"){
                visitor.answer = "It looks like your current debts are higher than they've been in recent months";
            } elif (here.name == "docs_to_upload_denial"){
                visitor.answer = "Ok no problem! Let me know if I can help with anything else";
            } elif (here.name == "kind_of_loan"){
                if("cred_score_num" in visitor.user_context["loan_profile"] && "homePreferences" in visitor.user_context["loan_profile"] && "ltv" in visitor.user_context["loan_profile"] && "loan_amount" in visitor.user_context["loan_profile"]){
                    ltv = visitor.user_context["loan_profile"]["ltv"];
                    loan_amount = visitor.user_context["loan_profile"]["loan_amount"];
                    credit_score = visitor.user_context["loan_profile"]["cred_score_num"];
                    veteran = visitor.user_context["loan_profile"]["homePreferences"]["veteran"];

                    loan_decision = hlp.loan_decision(ltv, credit_score, loan_amount, veteran);

                    visitor.answer = "After crunching the numbers, it looks like you can get approved for a "+ loan_decision.str +" loan. Are you interested in learning more about this type of loan?";
                }
            } elif (here.name == "kind_of_loan_confirmation"){
                if("cred_score_num" in visitor.user_context["loan_profile"] && "homePreferences" in visitor.user_context["loan_profile"]&& "ltv" in visitor.user_context["loan_profile"] && "loan_amount" in visitor.user_context["loan_profile"]){
                    ltv = visitor.user_context["loan_profile"]["ltv"];
                    loan_amount = visitor.user_context["loan_profile"]["loan_amount"];
                    credit_score = visitor.user_context["loan_profile"]["cred_score_num"];
                    veteran = visitor.user_context["loan_profile"]["homePreferences"]["veteran"];

                    loan_decision = hlp.loan_decision(ltv, credit_score, loan_amount, veteran);

                    loan_type = {
                        "Conventional": "https://www.experian.com/blogs/ask-experian/what-is-a-conventional-loan/#:~:text=A%20conventional%20loan%20is%20a,common%20type%20of%20mortgage%20loan.",
                        "FHA": "https://www.investopedia.com/terms/f/fhaloan.asp",
                        "USDA": "​​https://www.rd.usda.gov/programs-services/single-family-housing-programs/single-family-housing-guaranteed-loan-program",
                        "VA": "https://www.benefits.va.gov/homeloans/"
                    };

                    visitor.answer = "Of course! Here is some resource on that: " + loan_type[loan_decision];
                }
            }
            elif (here.name == "kind_of_loan_denial"){
                    visitor.answer = "No problem! Let me know if you have any further questions.";
            } else {
                if (visitor.answer == "") {
                    visitor.user_context["term_question_cnt"] = 0;
                    visitor.answer = "Okay sounds good. What else can I help with?";
                    # visitor.answer = "Is there anything else I could help you with?";
                }
            }
        }
    }

    # TODO: move this to a separate node
    can get_housing_price {
        # Replace with HLP API
        housing_price_db = {
            "Florida": "$400,000",
            "Seattle": "$560,000",
            "Michigan": "$530,000",
            "New York": "$745,000",
            "San Fran": "$1,200,000",
            "Average": "$550,000"
        };
        hit = 0;
        for i in housing_price_db.keys {
            if (i.str::lower in visitor.dialogue_context["location"].str::lower) {
                visitor.dialogue_context["price"] = housing_price_db[i];
                hit = 1;
                break;
            }
        }
        if (hit == 0){
            visitor.dialogue_context["price"] = housing_price_db["Average"];
        }
    }

    can log with talker exit {
        if(here.name != "conv_root_state"){
            if(visitor.answer){
                file.append_str('result.txt', "QUESTION: " + visitor.question + " INTENT: " + visitor.predicted_intent + " CONFIDENCE: " + visitor.intent_confidence.str + " EXTRACTED ENTITIES: " + visitor.extracted_entities.str + " RESPONSE: " + visitor.answer + " STATE: " + here.name + "\n");
            }
        }
    }
}


# Debug walkers
walker get_cand_intents {
    state{
        here::collect_intents;
        report here.cand_intents;
    }
}