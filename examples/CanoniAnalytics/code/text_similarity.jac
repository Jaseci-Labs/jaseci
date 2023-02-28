import {*} with './build_graph.jac';

#generate similary score for two blocks of sentences;
walker find_similar_sentences{

    can use.encode;
    can vector.cosine_sim;

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

walker get_actors_dialogue{
    has actors_dict = {};

    root{
         spawn here walker::build_graph;
         take-->;
    }

    location{
        take-->;
    }

    scene{
        childrens = -->node::actor;

        for item in childrens:
            {
                if item.name in actors_dict.dict.keys:
                    {
                        full_dialogue = actors_dict[item.name];
                        full_dialogue = full_dialogue + item.dialogue;
                        actors_dict.dict::update({(item.name).str : full_dialogue});
                    }
                actors_dict.dict::update({(item.name).str : item.dialogue.list});
            }
        take -->;
    }
    with exit {report actors_dict;}
}


walker get_actors_details{
    can file.load_json;
    has movie = file.load_json("movie_data.json");
    has actors_dict = {};

    for movie_scene in movie {
        content = movie[movie_scene];
        if content[1].type == dict:
            {
                actors_list = content[1].dict::keys;
                for _actor in actors_list:
                {
                    if _actor in actors_dict.dict::keys:
                    {
                        full_dialogue = actors_dict[_actor];
                        full_dialogue = full_dialogue + content[1][_actor];
                    }
                actors_dict.dict::update({(_actor).str : content[1][_actor].list});
                }
            }
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