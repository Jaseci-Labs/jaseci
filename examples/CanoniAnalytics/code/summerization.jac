import {*} with './build_graph_1.jac';

// generates the summary based on a corpse of text
walker summerizer {
    can bart_sum.summarize;
    has text;

    has summery = bart_sum.summarize(text=text, max_length=50, min_length=10);
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
        spawn here walker::summerizer(text=here.description);
        take -->;
    }
}
