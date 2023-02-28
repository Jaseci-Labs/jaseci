import {*} with './build_graph.jac';


walker get_actors_dialogue{
    has anchor actors_dict = {};

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


walker init{
    can sentiment.predict;

    has actors_details_dict = spawn here walker::get_actors_dialogue;

    for key in actors_details_dict:{
        sentiment.predict(actors_details_dict[key]);
    }

}