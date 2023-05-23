walker discussion_analysis {
    can bi_enc.get_context_emb;
    can bi_enc.get_candidate_emb;
    can bi_enc.dot_prod;
    can cl_summer.summarize;

    has text_in = "Hey i have a few questions about Tesla. First of all, how do I order a tesla? and if I already have a reservation, how do I configure my order? also, I would like to request a test drive and can you help me schedule that. Obviously that should happen before I put in any order. Oh one last thing, is there an easy way I can see all the options and design choices for the car?";
    has anchor responses = [];
    has transcripts = [
        "I think, I'm not sure if anyone can hear me, but I think the plant based foods and the traditional food is done sustainably are good ideas.",
        "Well pete seemed to cover um they're sustainable. They're plant based gluten free and dairy free.",
        "Just a question. Can anybody hear me?",
        "Yeah, I can hear you. Thank you.",
        "I'm personally not a fan of beats, but anyone else like beats by all means.",
        "I think the plant based food one is interesting, but I'm not sure if it's a trend that's here to stay. If it is. Um then that could be a way to go further that there's a lot of other people doing that.",
        "Plant based food is very popular in the pacific northwest of the United States, but where I'm at right now in the southern part. Not so much.",
        "Yeah. Yeah. Whereas I think I think perhaps some regional focus, their one imagines it's a stereotype, the traditional cooking, traditional recipes much more popular. Someone like the Southeast.",
        "Yeah. Yeah. Down here it's more about like fried foods, meats, things like that. Not so much about plants or free or anything like that. I do like the traditional foods done sustainably. I think um sustainable food is a good marketing pitch.",
        "Yeah, I think so. I think it's a key word that might resonate well with these customers.",
        "Well, certainly with younger people who are more concerned about sustainable practices such as myself.",
        "So the thing with these options that the food is going to cost more. Right. So how do you know? I think the key question is how do they how do this um company market their products so that it's you know, it's not about the increase in the price, but more about um you know, sustainability and so you know, better good of the planet and the community,",
        "If I'm not, if I'm not mistaken, and this is already a little bit more expensive than other brands and as long as they market it as being um at the very least like say 50, 70, 80% sustainable materials such as recycled paper and so forth. I think that would be justifiable. It's already a premium brand, I think.",
        "Mhm. So the idea of selling more traditional favorites, traditional foods done sustainably is an interesting one because I feel like that's probably the most realistic option in the near term, because I feel like with the plant based food and that was my idea, but I just felt like it's something that from the majority of people, it just, it just, you know, turns them off at least the people that I know, so it's it's more of a mental hurdle that people get over. But if people see traditional foods done more sustainably, like you guys just described, I feel like that's the more realistic approach that will get people to maybe pay a little bit more, but for food that they know they like the taste of it,",
        "how?",
        "are we defining traditional foods? How are you defining traditional foods when I think of traditional foods, I think of like fresh ingredients that you couldn't get in a boxed or traditionally, you know what Annie",
        "cells I was thinking of like macaroni and cheese, like traditional, like comfort foods. That's what I was thinking of. For some reason,",
        "I was just thinking about just any like regular food that is not like made from meat until this. So like I was, you know, like not plant based food for example, just like regular, normal food that everyone eats, but you know, it costs a little bit more because of, you know, the the responsible source and the thing",
        "that occurs to me is mostly the packaging. There's so much waste plastic involved in um like the things that you heat up in your microwave or whatever. Uh those things, it's always plastic plastic, plastic, if they could do that more sustainable in terms of the, like myself and my girlfriend who don't like excess plastic.",
        "I think what's interesting from the conversation is that the more sustainably idea encompasses a whole wide spread of different approaches and encompass everything from plastics to plant based foods.",
        "I think you're right about that sustainable food would mean adding something like plant based materials to um"
    ];
    # summarization
    all_text = "";
    for tran in transcripts {
        all_text += tran;
    }
    summaries = cl_summer.summarize(text=all_text, url="none", sent_count=3, summarizer_type="LsaSummarizer");

    # get embeddings
    context_embs = bi_enc.get_context_emb(transcripts);

    candidate_embs = bi_enc.get_candidate_emb(summaries);

    # cosine similarity
    for c in context_embs {
        max_sum = "";
        max_score = 0;
        for i=0 to i<summaries.length by i+=1 {
            score = bi_enc.dot_prod(c, candidate_embs[i]);
            if score > max_score {
                max_score = score;
                max_sum = summaries[i];
            }
        }
        responses.l::append(max_sum);
    }
    report responses;
}