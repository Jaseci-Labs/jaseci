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

node location{
    has location_name;
}

walker build_graph{
    can file.load_json;
    has movie = file.load_json("movie_data_sam.json");

    location_ext = spawn here ++> node::location(location_name="EXT");
    location_int = spawn here ++> node::location(location_name="INT");
    location_ext_int = spawn here ++> node::location(location_name="INT and EXT");

    for movie_scene in movie {
        scene_name = movie_scene;
        content = movie[movie_scene];

        scene_tag = scene_name.str::split(" ")[1];

        if content.type == str:
            description = content;
            if scene_tag == "EXT.":
                scene = spawn location_ext ++> node::scene(name=scene_name, description=description);
            elif scene_tag == "INT.":
                scene = spawn location_int ++> node::scene(name=scene_name, description=description);
            else:
                scene = spawn location_ext_int ++> node::scene(name=scene_name, description=description);

        if content.type == list:
            if content[0].type == str:
                description = content[0];
            if scene_tag == "EXT.":
                scene = spawn location_ext ++> node::scene(name=scene_name, description=description);
            elif scene_tag == "INT.":
                scene = spawn location_int ++> node::scene(name=scene_name, description=description);
            else:
                scene = spawn location_ext_int ++> node::scene(name=scene_name, description=description);

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

