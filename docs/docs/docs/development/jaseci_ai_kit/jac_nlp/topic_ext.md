---
sidebar_position: 1
title: Topic Extraction Model
description: Topic Modeling with Jaseci
---

# Topic Extraction Model

Topic Extraction (`topic_ext`)

Module `topic_ext` implemented for producing most relevant and possible set of topics for given set of text documents. Following is an example usage of the `topic_ext` module.

## Actions

* `topic_ext.topic_extraction`: This action extracts top n number of topics from each cluster. The the text along with cluster label for the text cluster should be provided here as an input.
  * Input
    * `texts` - (list of strings) list of input text documents.
    * `labels` - (list of int) list of labels associated with each text documents.
    * `n_topics` - (int) number of topics to extract from each cluster.
  * Returns
    * A dictionary which contains relevant topics for each clusters.

* **Input data file `topic_extraction.json`**
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

## Example Jac Usage:

```jac
walker init{
    can file.load_json;
    has text = file.load_json("topic_extraction.json");

    can use.encode;
    has encode = use.encode(visitor.text);

    can cluster.get_umap;
    final_features = cluster.get_umap(encode,2);

    can cluster.get_cluster_labels;
    labels = cluster.get_cluster_labels(final_features,"hbdscan",2,2);

    can topic_ext.topic_extraction;
    topic_dict = topic_ext.topic_extraction(texts=text,classes=labels,n_topics=5);
}
```

For a complete example visit [here](../../../../../tutorials/jaseci_ai_kit/jac_nlp/topic_ext)