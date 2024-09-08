import {*} with './build_graph.jac';

// generates the summary based on a corpse of text
walker summarizer {
    can bart_sum.summarize;
    has text;

    has summery = bart_sum.summarize(text=text, max_length=50, min_length=10);
}

// generates the keywords based on a corpse of text
walker keyword_generator{
    can topic_ext.keyword_extraction;
    has text;

    has keywords = topic_ext.keyword_extraction(sentence=text, n_words = 5, min_tokens = 1, max_tokens=1);
}

walker init{
    root{
         spawn here walker::build_graph;
         take-->;
    }

    location{
        take-->;
    }

    scene{
        spawn here walker::summarizer(text=here.description);
        spawn here walker::keyword_generator(text=here.description);
        take -->;
    }
}
