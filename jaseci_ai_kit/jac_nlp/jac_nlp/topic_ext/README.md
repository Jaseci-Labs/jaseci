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
    actions load module jac_nlp.topic_ext
    ```
3.  Load suplimentery modules in jac shell session
    ```
    actions load module jac_nlp.use_enc
    actions load module jac_misc.cluster
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

## **5. Extract topic for each clusters**

Use `topic_ext.topic_extraction` action to extract top n number of topics from each cluster.


**Parameters of `topic_ext.topic_extraction`**

- `texts` - (list of strings) list of input text documents.
- `labels` - (list of int) list of labels associated with each text documents.
- `n_topics` - (int) - Default 5 - number of topics to extract from each cluster.
- `min_tokens` - (int) - Default 1 - number of minimum words per topic.
- `max_tokens` - (int) - Default 2 - number of maximum words per topic.


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

Save the above full code in a file with name `topic_extraction.jac` and save the following text data inside the same directory with name `text_data.json`.

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

Run the jac code in the terminal with `jac run topic_extraction.jac` command. You will see the output as follows;

```json
{
  "success": true,
  "report": [
    {
      "0": [
        [
          "countries",
          0.392361531667182
        ],
        [
          "support",
          0.34487955266445003
        ],
        [
          "accounts",
          0.1934321572215864
        ],
        [
          "supporting",
          0.1934321572215864
        ],
        [
          "suppor",
          0.1934321572215864
        ]
      ],
      "1": [
        [
          "delivery",
          0.43893761248202734
        ],
        [
          "track",
          0.36634600373495724
        ],
        [
          "way",
          0.24618638191838274
        ],
        [
          "process",
          0.24618638191838274
        ],
        [
          "info",
          0.24618638191838274
        ]
      ],
      "2": [
        [
          "waiting",
          0.3358171700903774
        ],
        [
          "weeks",
          0.22567085009185084
        ],
        [
          "know",
          0.22567085009185084
        ],
        [
          "arrived",
          0.22567085009185084
        ],
        [
          "coming",
          0.22567085009185084
        ]
      ],
      "3": [
        [
          "new",
          0.5364793041447
        ],
        [
          "come",
          0.30089446678913445
        ],
        [
          "send",
          0.30089446678913445
        ],
        [
          "received",
          0.30089446678913445
        ],
        [
          "card",
          0.13515503603605478
        ]
      ]
    }
  ],
  "final_node": "urn:uuid:65d3bfac-c6d5-475c-8a18-3a221b507a4f",
  "yielded": false
}
```

## **6. Generate headings for each clusters**

Use `topic_ext.headline_generation` action to generate a relevant heading for each cluster.

**Parameters of `topic_ext.headline_generation`**

- `texts` - (list of strings) list of input text documents.
- `labels` - (list of int) list of labels associated with each text documents.


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
    topic_dict = topic_ext.headline_generation(texts=text,classes=labels);
}
```
Exepected output:

```json
{
  "success": true,
  "report": [
    {
      "0": "Countries Account Suppor",
      "1": "Track Card Delivery: Track Card Processing Delivery",
      "2": "Waiting Week Card Still Coming",
      "3": "Send New Card to New Address"
    }
  ],
  "final_node": "urn:uuid:e83f23f5-73d2-42a0-bebf-e87590e0db6e",
  "yielded": false
}
```
## **7. Extract keyword from a single document **

Use `topic_ext.keyword_extraction` action to generate a relevant heading for each cluster.

**Parameters of `topic_ext.keyword_extraction`**

- `sentence` - (list of strings) list of input text documents.
- `n_words` - (int) number of words or phrases to extract from each cluster..
- `min_tokens` - (int) - Default 1 - number of minimum words per topic.
- `max_tokens` - (int) Default 1 - number of maximum words per topic.
- `diversity` - (float) default 0.02 - The expected level of diversity. Increasing the diversity value will reduce the words with similar meaning in the resulted words list and the vise versa.


```jac
walker init{
    can topic_ext.keyword_extraction;
    has texts = "I like dogs";

    report topic_ext.keyword_extraction(sentence=texts, n_words=2, min_tokens = 1, max_tokens = 1, diversity = 0.02);
}
```

Exepected output:

```json
{
  "success": true,
  "report": [
    [
      "dogs",
      "like"
    ]
  ],
  "final_node": "urn:uuid:f91997c7-7d54-44ef-b238-2a8ea2f94418",
  "yielded": false
}
```
