walker cluster {
    can use.encode;
    can cluster.get_umap;

    has list_of_text;
    has anchor embeddings;

    embeddings = cluster.get_umap(text_embeddings=use.encode(list_of_text), n_components=2);

    report embeddings;
}