import {*} with './build_graph.jac';

// generates the summary based on a corpse of text
walker summerizer {
    can bart_sum.summarize;
    has text;
    has summery;

    summery = bart_sum.summarize(text, 20);
    std.out(summery);
}

walker init{
    root{
         spawn here walker::build_graph;
         take-->;
    }

    scene{
        spawn here walker::summerizer(text=here.description);
        take -->node::scene;
    }
}
