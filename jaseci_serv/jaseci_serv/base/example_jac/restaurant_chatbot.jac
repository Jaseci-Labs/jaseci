walker restaurant_chatbot {
    can bi_enc.get_context_emb;
    can bi_enc.get_candidate_emb;
    can bi_enc.dot_prod;
    can tfm_ner.extract_entity;
    # has user questions
    has user_question=[
        "i need you to confirm that there is a reservation under the name david kramer for 7:00 pm at pietro's"
    ];
    # has predefined intents
    has intents=[
        "cancel_reservation",
        "book_restaurant",
        "accept_reservations",
        "confirm_reservation"
    ];
    # uses bi_enc get_context_emb encode question
    question_embs=bi_enc.get_context_emb(user_question);
    # uses bi_enc get_canddiate_emb to encode intents
    intents_embs=bi_enc.get_candidate_emb(intents);
    # uses bi_enc dot produc to find the best suitable intents
    responses=[];
    for q_emb in question_embs:
        max_score = 0;
        best_answer = "";
        for i=0 to i<intents.length-1 by i+=1 {
            a_emb = intents_embs[i];
            sim_score = bi_enc.dot_prod(q_emb, a_emb);
            if sim_score > max_score {
                max_score = sim_score;
                matched_intent = intents[i];
            }
        }
        ent_resp=tfm_ner.extract_entity(user_question[0]);
        # uses tfm_ner extract_entity to find general entities
        resp={matched_intent:ent_resp};
        responses.l::append(resp);
    report responses;
}