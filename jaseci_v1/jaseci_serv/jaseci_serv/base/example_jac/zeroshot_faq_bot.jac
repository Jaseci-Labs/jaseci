walker zeroshot_faq_bot {
    can text_seg.get_segments;
    can use.question_encode;
    can use.answer_encode;
    can use.cos_sim_score;

    has text_in = "Hey i have a few questions about Tesla. First of all, how do I order a tesla? and if I already have a reservation, how do I configure my order? also, I would like to request a test drive and can you help me schedule that. Obviously that should happen before I put in any order. Oh one last thing, is there an easy way I can see all the options and design choices for the car?";
    has anchor responses = [];

    has answers = [
        "To configure your order, sign in to your Tesla Account and select manage on your existing reservation to configure your Tesla vehicle. Your original USD deposit has now been converted to SGD.",
        "Visit our Design Studio to explore our latest options and place your order. The purchase price and estimated delivery date will change based on your configuration.",
        "Yes, you can request for a test drive. Note: Drivers must be a minimum of 25 years of age and not exceeding 65 years of age, hold a full driving license with over 2 years of driving experience. Insurance conditions relating to your specific status must be reviewed and accepted prior to the test drive.",
        "Our team are ready to assist on Tesla.com via online chat.",
        "Model 3 and Model Y will qualify for the following: EV Early Adoption Incentive 45% rebate off the Additional Registration Fees (ARF) Capped at $20,000. Vehicular Emissions Scheme (VES) Tesla vehicles qualify under A1 band and will be eligible for a rebate of $25,000 off the Additional Registration Fees (ARF).",
        "Select the delivery pickup address in your Tesla Account and transfer the COE deposit of $10,000 via the method indicated in the COE Agreement.",
        "Yes. You can edit your design before your final invoice is issued in your Tesla Account. To log in to your Tesla Account, enter the email address and password you used to place your order. Any changes to your configuration may affect your delivery date.",
        "You can view your estimated delivery date in our Design Studio. The estimated delivery date depends on your configuration. Your Tesla Advisor will provide more specific timing closer to delivery.",
        "A cancellation request may be submitted within your Tesla Account. Please note that the order fee is non-refundable.",
        "A cancellation request may be submitted within your Tesla Account. The reservation deposit is fully refundable."
    ];

    # segmenet the input text into segments
    questions = text_seg.get_segments(text_in, 0.95);

    # for each segment, use use_qa to to get questions and answer embedding and then cosine similarity
    answer_embs = use.answer_encode(answers);
    question_embs = use.question_encode(questions);
    for q_emb in question_embs:
        max_score = 0;
        best_answer = "";
        for i=0 to i<answers.length-1 by i+=1 {
            a_emb = answer_embs[i];
            sim_score = use.cos_sim_score(q_emb, a_emb);
            if sim_score > max_score {
                max_score = sim_score;
                best_answer = answers[i];
            }
        }

        responses.l::append(best_answer);

    report responses;
}