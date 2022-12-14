# Text Cluster (cluster)

Module `cluster` implemented for clustering text document into similar clusters. This is a example program to cluster documents with jaseci `cluster` module. We will use input as list of raw text documents and will produce cluster labels for each text documents.

# **Walk through**

## **1. Import text cluster (`cluster`) module in jac**
1. For executing jaseci open terminal and run following command.
    ```
    jsctl -m
    ```
2.  Load `cluster` module in jac shell session
    ```
    actions load module jaseci_ai_kit.cluster
    ```
3. Load `use_enc` module in jac shell session
   ```
   actions load module jaseci_ai_kit.use_enc
   ```

## **2. Prepare text for clusters**

In this section, we'll take raw text as input, encode it, and then output a list of features with decreased dimensions. This can be utilized for further clustering in next section.

### **1. Load the text data**

Save the text data in `json` format.

```jac
walker features{
    can file.load_json;
    has text = file.load_json("text_data.json");
}
```

### **2. Create embeddings and reduce features**

In this section we are using use.encode jaseci module to encode raw text. The `use.encode` will return size of 512 vectors for each text document. We are reducing the dimention of vectors using `cluster.get_umap` action.

** Parameters of `cluster.get_umap`**

- `text_embeddings`: list -  This is a mandotory field. list of text embeddings should pass here.

- `n_neighbors`: int - By defauld this value is `15`. This is not a manodoty field, but if you want to get better out of this you have to set a value for this based on your input data. This parameter balances local versus global structure in the data. Low values will focus on local data points (will make an impact on the big picture), higher values will focus on the global data points (overall structure of the data)  (will lose fine details in the structure).

- `min_dist`: float - By default this value is 0.1. This is also not a mandotory field. This parameter controls how tightly `cluster.get_umap` is allowed to pack points together. Set this to low value when trying for clustering.

- `n_components`: int - The default value for this is 2, however it is not mandtory field. This represents the dimensionality of the reduced data. This is not limited 2 or 3 can try further like pca.

- `random_state`: int - By default this is 42. This represent the preproducability of the algorithm.

```jac
node feature_embedd{
    can use.encode;
    can cluster.get_umap;
    has final_features;

    can  set_features with features entry{
        encode = use.encode(visitor.text);
        final_features = cluster.get_umap(encode,2);
    }
}
```

## **3. Get cluster labels**

We will obtain cluster labels for each text document in this section. The output from the previous section is the input here. To get cluster lables we are using `cluster.get_cluster_labels`  action.

**Parameters of `cluster.get_cluster_labels`**

- embeddings: list - This accept list of embedded text features, this is a mandotory field.

- algorithm: str - By default the value of this is "hbdscan". So far jaseci only support `hbdscan` and `kmeans` algorithms for clutering.

- min_samples: int - This is a mandotory field if only you are using `hbdscan` algorithm. The minimum number of data points in a cluster is represented here. Increasing this will reduces number of clusters.

- min_cluster_size: int - This is a mandotory field if only you are using `hbdscan` algorithm. This represents how conservative you want your clustering should be. Larger values more data points will be considered as noise
- n_clusters: int - This is also a mandotory field if only you are using `kmeans` algorithm. This defines how many number of clusters you need.

```jac
can cluster.get_cluster_labels;
has labels;

has final_features;

can set_lables{
    labels = cluster.get_cluster_labels(embeddings=final_features,algorithm="hbdscan",min_samples=2,min_cluster_size=2);
    report labels;
    }
```

If you are going to use `kmeans` algorithm, the `set_lables` ability should be as follows;

```
can set_lables{
    labels = cluster.get_cluster_labels(embeddings=final_features,algorithm="kmeans",min_samples=0,min_cluster_size=0,n_clusters=2);
    report labels;
    }
```

## **4. Wrapping up all together**

The complete code with the graph structure.

```jac
graph text_cluster_graph {
    has anchor text_feature;
    spawn {
        text_feature = spawn node::feature_embedd;
        text_cluster = spawn node::cluster_labels;
        text_feature -[cluster_model(model_type="hbdscan")]-> text_cluster;
    }
}

node feature_embedd{
    can use.encode;
    can cluster.get_umap;
    has final_features;

    can  set_features with features entry{
        encode = use.encode(visitor.text);
        final_features = cluster.get_umap(encode,2);
    }
}

node cluster_labels{
    can cluster.get_cluster_labels;
    has labels;
}

edge cluster_model{
    has model_type;
}

walker features{
    can file.load_json;
    has text = file.load_json("text_data.json");
}

walker init{
    has final_features;

    can set_lables{
    labels = cluster.get_cluster_labels(embeddings=final_features,algorithm="hbdscan",min_samples=2,min_cluster_size=2);
    report labels;
    }

    root {
        spawn here --> graph::text_cluster_graph;
        take-->;
    }

    feature_embedd{
        spawn here walker::features;
        final_features = here.final_features;
        take-->;
    }

    cluster_labels{
        ::set_lables;
    }
}

```

Save the above code in a file with name `cluster.jac` and save the following text data inside the same directory.

```json
[
    "still waiting card",
    "countries supporting",
    "card still arrived weeks",
    "countries accounts suppor",
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
    "countries currently support"
]
```

Run the jac code in the terminal with `jac run cluster.jac` command. You will see the output as follows;

```
{
  "success": true,
  "report": [
    [
      0,
      2,
      0,
      2,
      2,
      0,
      3,
      2,
      0,
      1,
      1,
      3,
      1,
      3,
      2
    ]
  ],
  "final_node": "urn:uuid:8828d927-044d-4dec-85b4-65ba34e4a93c",
  "yielded": false
}
```









