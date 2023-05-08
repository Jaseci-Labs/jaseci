walker virtual_assistant {
    can text_seg.get_segments;
    can bi_enc.infer;
    can tfm_ner.extract_entity;
    can sbert_sim.get_text_sim;
    can use.qa_classify;
    has threshold=0.9;
    # has a article
    has article="The geopolitics of knowledge is shifting. The 19th annual edition of the Times Higher Education World University Rankings, published on 12 October, demonstrates an accelerating trend: the USs share of the worlds top 100 universities is declining, while that of East Asian nations, led by China, and universities in the Middle East is on the rise. trends that will shape the future of higher education These 12 innovators are transforming the future of education A view from China on the future of innovation and education In 2018, the US boasted close to half of the worlds top 100 positions in the world rankings, with 43 universities. In todays edition, the US has just 34, as household names like Dartmouth College, and great regional powerhouse universities including Ohio State and Michigan State lose their top 100 status. Meanwhile, mainland Chinas share of the world top 100 positions has risen from just two in 2018, to an impressive seven today. Hong Kong has a further five top 100 institutions, up from just three in 2018. South Korea has three top 100 places, up from two in 2018. Singapore and Japan both takes two top 100 places each. best universities in the world Times Higher Education World University Rankings China's Tsinghua University ranks 16 among the best universities in the world, while it tops in Asia. In the Middle East, Saudi Arabia and the United Arab Emirates are leading what some are calling a new renaissance driven by innovation and knowledge creation, backed by heavy investment. Saudis King Abdulaziz University is one of the fastest-rising universities in the world, rocketing to 101st position this year from 190th last year, and the Kingdom is the most improved nation, by national average score, in the world rankings this year. In the UAE, of the six UAE universities included in the overall world rankings for 2023, five are on the rise led by the United Arab Emirates University and the University of Sharjah, which have both surged this year into the world's top 300 list. Shifts in global innovation and knowledge economy. The Times Higher Educations (THE) world ranking has become a closely watched barometer of the shifts in the global innovation and knowledge economy, supporting governments policymaking and university leaders strategic decisions, as well as supporting millions of internationally-mobile students to decide on who to trust with their education. The World University Rankings are based on 13 separate performance metrics, covering the full range of internationally-focussed research universities core missions: teaching, research, knowledge transfer and international outlook. The 2023 edition is based on an analysis of over 15.5 million research publications and over 112 million citations to those publications as well as a survey of more than 40,000 academics worldwide on the international academic reputation of each school, on top of data on institutional income and faculty demographics, including international talent recruitment and research collaboration. What is the World Economic Forum doing about shaping the future of the Arab region? So, should the data be a cause for alarm for the US and its Western allies in an increasingly polarised world? No, says Simon Marginson, professor of higher education at the University of Oxford, because there are simply more outstanding universities in the world and a rising tide lifts all boats. Theres no evidence that US research is weakening in an absolute sense, Marginson told Times Higher Education. This continues to be the most prestigious system in the world. But where there is cause for mounting concern is in the fear that increasing geopolitical tensions and mistrust means the world as a whole does not fully benefit from the overall boom in global research excellence, as systems retreat into nationalism and knowledge sharing shrinks back. For example, while Chinas universities excel and rise up the rankings, their scores for international research collaboration and their share of international talent are in decline. It would be regrettable if the growth of foreigners working in higher education in China has stopped as the engagement is good for everyone, Marginson told However, it would be unsurprising, as we are now in a more conflictual era in the geopolitics of higher education. Top of the (university) class Top of the World University Rankings for the seventh consecutive year, is a university renowned for its international knowledge sharing the UKs University of Oxford. Oxford is followed by Harvard University in second, while the University of Cambridge (up from 5th) and Stanford University (up from 4th) share third place. The Massachusetts Institute of Technology holds fifth place. In a further nod to the US decline, the University of Chicago has lost its world top-10 place, falling to 13th, with the UKs Imperial College London taking its place, moving up from 12th last year, to 10th in 2023. Times Higher Education World University Rankings best universities in the world Most US institutes take top spots in the best universities in the world rankings by the Times Higher Education. Oxfords vice chancellor Louise Richardson said in a statement: My colleagues and I are absolutely delighted that for the seventh consecutive year Oxford has been named the top university in the world. I am very grateful to those who work on compiling these rankings which prove so helpful to universities. Above all, I am indebted to the extraordinary women and men of Oxford whose research and teaching continues to excite our imaginations, broaden our horizons, cure disease and explore deeply difficult problems for the betterment of society. I am so proud to be associated with them.";
    # has predefined intent
    has intents=[
        "global innovation",
        "top university",
        "knowledge economy",
        "comparing fees",
        "picking the best school",
        "evaluating your journey"
        ];
    # has prefineded entities
    has entities=[
        "university name",
        "company name",
        "person name",
        "time range"
        ];
    responses=[];
    # uses text_seg get_segments to get segments from article returns list of text sent
    segments=text_seg.get_segments(article,threshold);

    for segment in segments:
        # uses bi_enc infer each segments intent for for each sent
        pred_intent=bi_enc.infer(segment, intents, "text", "text");
        pred_sbert=sbert_sim.get_text_sim([segment], intents, 1);
        # uses tfm_ner extract_entity to find general predifined entities from each segment
        fallback_ents=tfm_ner.extract_entity(segment);
        // # uses ent_ext entity_detection to get fallback entities
        // pred_ents=ent_ext.entity_detection(segment,entities);
        # uses use qa_classify to classify the intents for fallback
        fallback_intent=use.qa_classify(segment,intents);
        resp={
            pred_intent[0]["predicted"]["label"]:fallback_ents,
            fallback_intent["match"]:fallback_ents
        };
        responses.l::append(resp);
    report responses;

}