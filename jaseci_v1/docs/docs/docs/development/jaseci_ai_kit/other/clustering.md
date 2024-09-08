---
sidebar_position: 1
title: CLustering Module
description: Text Clustering with Jaseci.
---

# Clustering Module

Module `cluster` implemented for clustering text document into similar clusters. This is a example program to cluster documents with jaseci `cluster` module. We will use input as list of raw text documents and will produce cluster labels for each text documents.

## Actions

* `get_umap`: Reducing the dimension of data while preserving the relationship between data points to identify clusters easier.
    * Input
        * `text_embeddings` (list): list of text embeddings should pass here.
        * `n_neighbors` (int): number of neighbors to consider.
        * `min_dist` (float): minimum distance between clusters.
        * `n_components` (int): the dimensionality of the reduced data.
        * `random_state`(int): pre-producibility of the algorithm.

    * Returns: multi-dimensional array of reduced features.

* `get_cluster_labels`: To get list of possible cluster labels
    * Input
        * `embeddings`(list): This accept list of embedded text features.
        * `algorithm` (String): Algorithm for clustering.
        * `min_samples` (int): The minimum number of data points in a cluster is represented here. Increasing this will reduces number of clusters
        * `min_cluster_size` (int): This represents how conservative you want your clustering should be. Larger values more data points will be considered as noise

    * Returns: list of labels.


## Example Jac Usage

**Input data file `text_cluster.json`**
```json
  [
    "still waiting card",
    "countries supporting",
    "card still arrived weeks",
    "countries accounts support",
    "provide support countries",
    "waiting week card still coming",
    "track card process delivery",
    "countries getting support",
    "know get card lost",
    "send new card",
    "still received new card",
    "info card delivery",
    "new card still come",
    "way track delivery card",
    "countries currently support"]
```

```jac
walker text_cluster_example{
    can file.load_json;
    can use.encode;
    can cluster.get_umap;
    can cluster.get_cluster_labels;

    has text, encode, final_features, labels;

    text = file.load_json("text_cluster.json");
    encode = use.encode(text);
    final_features = cluster.get_umap(encode,2);

    labels = cluster.get_cluster_labels(final_features,"hbdscan",2,2);
    std.out(labels);

}
```

For a complete example visit [here](../../../../../tutorials/jaseci_ai_kit/jac_nlp/cluster)