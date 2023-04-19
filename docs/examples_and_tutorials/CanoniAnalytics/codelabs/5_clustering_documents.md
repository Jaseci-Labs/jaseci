# Find Similar clusters in a set of documents

Text clustering, also known as text grouping or document clustering, is a technique used in natural language processing (NLP) and machine learning to categorize large sets of unstructured textual data into meaningful groups or clusters. The goal of text clustering is to identify patterns and relationships within the text that can be used to group similar documents together based on their content, topics, or other features. This can help researchers, businesses, and organizations to better understand the underlying structure of their textual data and to identify important insights or trends that may be hidden within it. Text clustering is often used in applications such as document organization, information retrieval, and text summarization.


- [Find Similar clusters in a set of documents](#find-similar-clusters-in-a-set-of-documents)
  - [Loading the data](#loading-the-data)
  - [Clustering the dialogue data](#clustering-the-dialogue-data)
  - [Topic modeling from clustered data.](#topic-modeling-from-clustered-data)

## Loading the data

In this section, we will retrieve the dialogues from the raw `JSON` file. This approach is more efficient than traversing a graph to gather the data because here we need to gather all the dialogues in a scene into a single list.

```jac
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
                    dialogues.list::append(_dialogue);
                }
            }
    }
    with exit {report dialogue;}
}
```

- `can file.load_json;` and `has movie = file.load_json("movie_data.json");` to load the data from the `JSON` file.
- `has anchor dialogue;` we are using anchor keyword because we want to use this loaded data from outside of the `load_data` walker.
- `for` loops and other programming concepts are similar to the general programming languages so I'm not going to explain them in detail.
- `with exit {report dialogue;}` This will bring back the dialogue list that was made when the walker left.

## Clustering the dialogue data

Now that we have put the data into a list, our next step is to group these text documents into clusters.

```jac
walker get_dialog_clusters{

    can cluster.get_umap;
    can cluster.get_cluster_labels;

    can sbert_sim.load_model;
    can sbert_sim.getembeddings;

    has final_features;
    has anchor cluster_lables;

    _dialogue = spawn here walker::load_data;

    encode = sbert_sim.getembeddings(_dialogue);

    final_features = cluster.get_umap(encode,25);
    cluster_lables = cluster.get_cluster_labels(embeddings=final_features,algorithm="hbdscan",min_samples=10,min_cluster_size=5);

    with exit {report cluster_lables;}
}
```

- `can cluster.get_umap;` imports UMAP dimensionality reduction algorithm.
- `can cluster.get_cluster_labels;` import clustering agorithm.
- `can sbert_sim.load_model;` and `can sbert_sim.getembeddings`  to import the `sbert` modules `load_model` and `getembeddings` functionalities respectively.
- `_dialogue = spawn here walker::load_data;` here we are calling the `load_data` walker and assigning the loaded dialogue data to a variable names `_dialogue`.
- `encode = sbert_sim.getembeddings(_dialogue);` we encoding the dialogues using the `sbert` encoder.
- `final_features = cluster.get_umap(encode,3);` the encoded data is in 512 dimension, which is very unefficient and difficult to handle by machine learning algorithms. so we are reducing the dimension of data to three dimensions.
- `cluster_lables = cluster.get_cluster_labels(embeddings=final_features,algorithm="hbdscan",min_samples=10,min_cluster_size=5);` clusteing documents with HBDSCAN algorithm.

Save all the codes in a one file and run to see the output. You have to load `sber_sim` from `jac_nlp` package and `cluster` from `jac_misc` package befor running the code.

```bash
actions load module jac_nlp.sbert_sim
actions load module jac_misc.cluster
```

Here you may notice we don't have an `init` walker. So we have to specify which walker to run when executing the program.

```
jac run cluster.jac -walk get_dialog_clusters
```

if everything is fine you may see an output similar to this. these are the cluster labels.

```
  [
      -1,
      -1,
      -1,
      1,
      -1,
      1,
      -1,
      1,
      -1,
      3,
      3,
      -1,
      -1,
      1,
      .
      .
    ]
```

## Topic modeling from clustered data.

Topic modeling is a statistical method used in natural language processing (NLP) to identify latent topics or themes present in a large corpus of text data. The goal of topic modeling is to uncover the underlying structure and patterns in the text data, and to group similar documents together based on their content.

Topic modeling algorithms typically work by analyzing the frequency and co-occurrence of words in the text, and identifying clusters of words that tend to appear together. These clusters are then assigned labels or "topics" that describe the dominant themes within them.

Topic modeling has many applications in text analysis, including information retrieval, content recommendation, and sentiment analysis. It can also be used to identify emerging trends and patterns in large datasets, and to support decision-making in fields such as marketing, finance, and healthcare.

In this section we are going to extract topics from the already clustered documents.

```jac
walker get_topics{

    can topic_ext.topic_extraction;

    documents = spawn here walker::load_data;
    labels = spawn here walker::get_dialog_clusters;

    topic_dict = topic_ext.topic_extraction(texts=documents,classes=labels,n_topics=5);

    report topic_dict;
}
```

- `can topic_ext.topic_extraction;` importing topic extraction functionality.
- `documents = spawn here walker::load_data;` here we are calling the `load_data` walker and assigning the loaded dialogue data to a variable names `_dialogue`.
- `labels = spawn here walker::get_dialog_clusters;` and here we are calling the `get_dialog_clusters` walker to get clustered labels.
- `topic_dict = topic_ext.topic_extraction(texts=documents,classes=labels,n_topics=5);` extracting topics for each clusters. We are extracting top 5 topics from each cluster here.

Before running this program you have to load the `jac_nlp.topic_ext` module.

```
actions load module jac_nlp.topic_ext
jac run cluster.jac -walk get_topics
```
Thw output should be something like this;

```
 "-1": [
        [
          "volstagg",
          0.00885220102649983
        ],
        [
          "don",
          0.007081511466296675
        ],
        [
          "darcy",
          0.006750459936849765
        ],
        [
          "just",
          0.006218810516793914
        ],
        [
          "know",
          0.00597414959400658
        ]
      ],
      "0": [
        [
          "belt",
          0.06428909489091844
        ],
        .
        .
        .
        .
```






