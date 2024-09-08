import {*} with './build_graph.jac';

#generate similary score for two blocks of sentences;
walker find_similar_sentences{

    can sbert_sim.load_model;
    can sbert_sim.getembeddings;
    can vector.cosine_sim;

    has dialogue_1;
    has dialogue_2;
    has sim_value;

    sbert_sim.load_model();

    phrase_1 = "";
    for lot in dialogue_1:
        phrase_1 = phrase_1 + ' ' + lot;

    phrase_2 = "";
    for lot in dialogue_2:
        phrase_2 = phrase_2 + ' ' + lot;

    encode1 = sbert_sim.getembeddings(phrase_1);
    encode2 = sbert_sim.getembeddings(phrase_2);

    sim_value =  vector.cosine_sim(encode1,encode2);
    if sim_value >= 0.6:
    {
        std.out(sim_value);
        std.out("phrase 1 :",phrase_1);
        std.out("phrase 2 :",phrase_2);
    }
}


walker init{
    has _list;
    has sim_value;

    root{
         spawn here walker::build_graph;
         take-->;
    }

    location{
        take-->;
    }

    scene{
        childrens = -->node::actor;

        if childrens.length > 1:
        {
            _list = childrens.dialogue;
            pairslist = _list.list::pairwise;
            for item in pairslist:
                spawn here walker::find_similar_sentences(dialogue_1=item[0], dialogue_2=item[1]);
        }
        take -->;
    }
}