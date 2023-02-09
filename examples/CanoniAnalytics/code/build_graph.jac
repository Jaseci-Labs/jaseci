node root;

node scene{
    has name;
    has description;
    has desc_summery;

    can set_summery with summerizer entry{
        here.desc_summery = visitor.summery;
    }
}

node actor{
    has name;
    has dialogue;
    has dialogue_summery;

    can set_summery with summerizer entry{
        here.dialogue_summery = visitor.summery;
    }
}

walker build_graph{
    can file.load_json;
    has movie = file.load_json("movie_data.json");
    for movie_scene in movie {
        scene_name = movie_scene;
        content = movie[movie_scene];

        if content.type == str:
            description = content;
            scene = spawn here ++> node::scene(name=scene_name, description=description);

        if content.type == list:
            if content[0].type == str:
                description = content[0];
            scene = spawn here ++> node::scene(name=scene_name, description=description);

            if content[1].type == dict:
                for actor in content[1]{
                    name = actor;
                    dialogue = content[1][actor];
                        spawn scene ++>node::actor(name=name, dialogue=dialogue);
                    }
        }
}

walker init{
    root{
         spawn here walker::build_graph;
    }
}

