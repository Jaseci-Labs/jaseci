# Topic Extraction Model (topic_ext)

Module `topic_ext` implemented for extracting topics from set of documents. This module accepts as input a set of documents and their associated class labels. You may use Jaseci `cluster` module to cluster document list to similar groups. This is an example code to demostrate `topic_ext` module.

# **Walk through**

## **1. Import text cluster (`topic_ext`) module in jac**
1. For executing jaseci open terminal and run following command.
    ```
    jsctl -m
    ```
2.  Load `topic_ext` module in jac shell session
    ```
    actions load module jaseci_ai_kit.topic_ext
    ```

## **2. Prepare text for clusters**

In this section, we'll take raw text as input, encode it, cluser it and then out put a list of cluster labels associate with each text document.

### **1. Load the text data**

Save the text data in `json` format.

```jac
walker init{
    can file.load_json;
    has text = file.load_json("text_data.json");

    can use.encode;

    has encode = use.encode(visitor.text);
}
```

### **2. Create embeddings**

Use `use_enc` module to encode documents.
```jac
walker init{
    can file.load_json;
    has text = file.load_json("text_data.json");

    can use.encode;
    has encode = use.encode(visitor.text);
}
```

### **3. Reduce dimensions using umap**

Use `cluster.get_umap` action to reduce features.

```jac
walker init{
    can file.load_json;
    has text = file.load_json("text_data.json");

    can use.encode;
    has encode = use.encode(visitor.text);

    can cluster.get_umap;
    final_features = cluster.get_umap(encode,2);

}
```

### **4. Cluster documents and get document lables**

Use `cluster.get_cluster_labels` to get cluster labels.

```jac
walker init{
    can file.load_json;
    has text = file.load_json("text_data.json");

    can use.encode;
    has encode = use.encode(visitor.text);

    can cluster.get_umap;
    final_features = cluster.get_umap(encode,2);

    can cluster.get_cluster_labels;
    labels = cluster.get_cluster_labels(final_features,"hbdscan",2,2);
}
```

## **3. Extract topic for each clusters**

Use `topic_ext.topic_extraction` action to extract top n number of topics from each cluster.

```jac
walker init{
    can file.load_json;
    has text = file.load_json("text_data.json");

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

**Parameters of `topic_ext.topic_extraction`**

- `texts` - (list of strings) list of input text documents.
- `labels` - (list of int) list of labels associated with each text documents.
- `n_topics` - (int) number of topics to extract from each cluster.