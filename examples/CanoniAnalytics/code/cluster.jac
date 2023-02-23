walker get_dialog_clusters{
    can cluster.get_umap;
    can cluster.get_cluster_labels;
    can sbert_sim.load_model;
    can use.encode;

    has movie = file.load_json("movie_data.json");

    dialogues = [];

    for movie_scene in movie {
        content = movie[movie_scene];
        if content[1].type == dict:
            {
                actors_list = content[1].dict::keys;
                for _actor in actors_list:
                {
                    _dialogue = " ".str::join(content[1][_actor]);
                    dialogues.list::append(_dialogue);
                }
            }
        }

    encodes = use.encode(dialogues);
    cluster_lables = cluster.get_umap(encodes,25);
    report cluster_lables;
}
