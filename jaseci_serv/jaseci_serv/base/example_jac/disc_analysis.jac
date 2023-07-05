walker disc_analysis {
    can sbert_sim.getembeddings;
    can sbert_sim.get_dot_score;
    can cl_summer.summarize;
    has anchor responses = [];
    has transcripts = [
        "I think, I'm not sure if anyone can hear me, but I think the plant based foods and the traditional food is done sustainably are good ideas.",
        "Well pete seemed to cover um they're sustainable. They're plant based gluten free and dairy free.",
        "Just a question. Can anybody hear me?",
        "Yeah, I can hear you. Thank you.",
        "I'm personally not a fan of beats, but anyone else like beats by all means."
        ];
    # summarization
    all_text = "";
    for tran in transcripts {
        all_text += tran;
    }
    summaries = cl_summer.summarize(text=all_text, url="none", sent_count=3, summarizer_type="LsaSummarizer");

    # get embeddings
    context_embs = sbert_sim.getembeddings(transcripts);

    candidate_embs = sbert_sim.getembeddings(summaries);
    # cosine similarity
        max_sum = "";
        max_score = 0;
        for i=0 to i<summaries.length by i+=1 {
            score = sbert_sim.get_dot_score(context_embs[i], candidate_embs[i]);
            if score[0][0] > max_score {
                max_score = score[0][0];
                max_sum = summaries[i];
                responses.l::append(max_sum);
            }
        }
    report responses;
}