walker flight_chatbot {
    can use.question_encode;
    can use.answer_encode;
    can use.dist_score;
    can ent_ext.entity_detection;
    # has user questions
    has user_question=[
        "on united airlines give me the flight times from boston to dallas"
    ];
    # has predefined answers
    has answers=[
        "Here are the list of flight that travels every day, 1. united airlines, 2. qatar airways, 3. american airlines",
        "the united airlines travels on every wenesday at 9:00pm from boston to dallas",
        "we provide the car rentals in baltimore",
        "american airlines serves between denver pittsburgh and atlanta",
        "qatar airways serve atlanta",
        "the arrival time in san francisco for the united airlines is 7:55 am",
        "the flights from san diego to houston is not available curently",
        "round trip fares from pittsburgh to philadelphia is 1000 dollars",
        "the 8 am flight from san francisco to atlanta uses boeing 737"
    ];
    # has prefineded entities
    has entities=[
        "flight_number",
        "timeRange",
        "price",
        "city",
        "airline_name"
        ];
    responses=[];
    # uses use question to encode question
    question_embs = use.question_encode(user_question);
    # uses use answer to encode answer
    answer_embs = use.answer_encode(answers);
    # uses use dist_score to find the best suitable answer
    for q_emb in question_embs:
        max_score = 0;
        best_answer = "";
        for i=0 to i<answers.length-1 by i+=1 {
            a_emb = answer_embs[i];
            sim_score = use.dist_score(q_emb, a_emb);
            if sim_score > max_score {
                max_score = sim_score;
                matched_intent = answers[i];
            }
        }
        # uses ent_ext entity_detection to find the entities
        ent_resp=ent_ext.entity_detection(matched_intent,entities);
        resp={matched_intent:ent_resp};
        responses.l::append(resp);
    report responses;

}