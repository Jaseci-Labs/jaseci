node root;

# scene node and it's attributes
node scene{
    has id;
    has name;
    has description;
    has desc_summary;
    has keywords;

    can set_summary with summarizer entry{
        here.desc_summary = visitor.summery;
    }

    can set_keywords with keyword_generator entry{
        here.keywords = visitor.keywords;
    }
}

# edges conecting scene nodes to actors
edge acts;

# actor node and it's attributes
node actor{
    has name;
    has dialogue;
}

# location node and it's attributes
node location{
    has location_name;
}


# walker building the graph
walker build_graph{
    can file.load_json;
    has movie = file.load_json("movie_data.json");

    location_ext = spawn here ++> node::location(location_name="EXT");
    location_int = spawn here ++> node::location(location_name="INT");
    location_ext_int = spawn here ++> node::location(location_name="INT and EXT");

    for movie_scene in movie {
        _scene_name = movie_scene;
        content = movie[movie_scene];

        scene_tag = _scene_name.str::split(" ")[1];
        scene_id = _scene_name.str::split(" ")[0];
        scene_name = _scene_name.str::split("T.")[-1];

        if content.type == str:
            description = content;
            if scene_tag == "EXT.":
                scene = spawn location_ext ++> node::scene(id=scene_id, name=scene_name, description=description);
            elif scene_tag == "INT.":
                scene = spawn location_int ++> node::scene(id=scene_id, name=scene_name, description=description);
            else:
                scene = spawn location_ext_int ++> node::scene(id=scene_id, name=scene_name, description=description);

        if content.type == list:
            if content[0].type == str:
                description = content[0];
            if scene_tag == "EXT.":
                scene = spawn location_ext ++> node::scene(id=scene_id, name=scene_name, description=description);
            elif scene_tag == "INT.":
                scene = spawn location_int ++> node::scene(id=scene_id, name=scene_name, description=description);
            else:
                scene = spawn location_ext_int ++> node::scene(id=scene_id, name=scene_name, description=description);

            if content[1].type == dict:
                for _actor in content[1]{
                        name = _actor;
                        dialogue = content[1][_actor];

                        spawn scene +[acts]+>node::actor(name=name,dialogue=dialogue);
                    }
        }
}

walker init{
    root{
         spawn here walker::build_graph;
    }
}

