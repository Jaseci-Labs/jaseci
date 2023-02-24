walker load_data{
    can file.load_json;
    has movie = file.load_json("movie_data.json");
    has anchor dialogue;

    dialogue = [];

    for movie_scene in movie {
        content = movie[movie_scene];
        if content[1].type == dict:
            {
                actors_list = content[1].dict::keys;
                for _actor in actors_list:
                {
                    _dialogue = " ".str::join(content[1][_actor]);
                    dialogue.list::append(_dialogue);
                }
            }
    }
    report dialogue;
}


walker get_dialog_clusters{

    can cluster.get_umap;
    can cluster.get_cluster_labels;

    can sbert_sim.load_model;
    can sbert_sim.getembeddings;

    can use.encode;
    has final_features;
    has anchor cluster_lables;

    _dialogue = spawn here walker::load_data;

    encode = sbert_sim.getembeddings(_dialogue);
    final_features = cluster.get_umap(encode,25);
    cluster_lables = cluster.get_cluster_labels(embeddings=final_features,algorithm="hbdscan",min_samples=10,min_cluster_size=5);

    with exit {report cluster_lables;}
}

walker get_topics{

    can topic_ext.topic_extraction;

    documents = spawn here walker::load_data;
    labels = spawn here walker::get_dialog_clusters;

    topic_dict = topic_ext.topic_extraction(texts=documents,classes=labels,n_topics=5);

    report topic_dict;
}