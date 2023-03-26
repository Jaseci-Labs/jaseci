# Analyse sentiments in Dialogues

Sentiment analysis is a process of analyzing text data to determine the emotional tone or attitude expressed in it. It involves using natural language processing and machine learning techniques to identify and extract subjective information from text, such as opinions, attitudes, and emotions. Sentiment analysis is commonly used in social media monitoring, customer feedback analysis, brand reputation management, and market research. It can help organizations gain insights into customer sentiment, identify emerging trends, and make data-driven decisions. Sentiment analysis can be performed at different levels, including document-level, sentence-level, and aspect-level analysis. The output of sentiment analysis is typically a numerical score or a categorical label that indicates the polarity of the text, such as positive, negative, or neutral.

- [Analyse sentiments in Dialogues](#analyse-sentiments-in-dialogues)
  - [Loading the data](#loading-the-data)
  - [Predicting the sentiment in sentences](#predicting-the-sentiment-in-sentences)

## Loading the data

As we mapped the `JSON` data to a graph in a previous section, we are going to use the same graph to collect the dialogue expressed by every actor in the movie. So we have to import the `guild_graph.jac` code into our sentiment analysis code.

```jac
import {*} with './build_graph.jac';
```
Next, we will create a walker to collect the data while traversing through the nodes of the graph.

```jac
walker get_actors_dialogue{
    has anchor actors_dict = {};

    root{
         spawn here walker::build_graph;
         take-->;
    }

    location{
        take-->;
    }

    scene{
        children = -->node::actor;

        for item in children:
            {
                if item.name in actors_dict.dict.keys:
                    {
                        full_dialogue = actors_dict[item.name];
                        full_dialogue = full_dialogue + item.dialogue;
                        actors_dict.dict::update({(item.name).str : full_dialogue});
                    }
                actors_dict.dict::update({(item.name).str : item.dialogue.list});
            }
        take -->;
    }
    with exit {report actors_dict;}
}
```
- `has anchor actors_dict = {};` defining an anchor to store the dialogue dictionary.
- `spawn here walker::build_graph;` spawning the graph from the root.
- `children = -->node::actor;`get all the `actor` nodes attached to the current `scene` node in which `get_actors_dialogue` walker is in.
- `if item.name in actors_dict.dict.keys:` is to check whether we already added the actor into `actors_dict` if it's already added we append only the dialogue to that actor. if not we are adding the `item.name` as key and `item.dialogue` as the value to the dictionary in line `actors_dict.dict::update({(item.name).str : item.dialogue.list});`
- `with exit {report actors_dict;}` returns the `actor_dict` when the walker exits from the graph.

## Predicting the sentiment in sentences

In this section, we are going to do sentiment analysis for the dialogues of every actors. For this we are using Jaseci `sentiment` module.

```jac
walker init{
    can sentiment.predict;
    has actors_details_dict = spawn here walker::get_actors_dialogue;

    for key in actors_details_dict:{
        try:{
            texts = actors_details_dict[key];
            pred = sentiment.predict(texts);
            std.out(pred);
        }

        else with error{
            std.out(error);
        }
}
}
```

- `can sentiment.predict;` importing the sentiment prediction action.
- `has actors_details_dict = spawn here walker::get_actors_dialogue;` assigning the reported values from `get_actors_dialogue` walker to a variable named `actors_details_dict`
- `for key in actors_details_dict:`  looping through keys in `actors_details_dict` dictionary.
- `pred = sentiment.predict(texts);` predicting the sentiment of the texts.
- You may have noticed in this code snippet we have included exception handling. In Jaseci exceptions can be handled by `try {}` and `else with error {}`.


Save all these code snippets in a one `jac` file. Before executing this code we have to load `sentiment` action in the `jsctl` shell.

```
actions load module jac_nlp.sentiment
jac run jac run sentiment_analysis.jac
```

If everything is fine you will see an output similar to following.

```
[{"label": "NEU", "score": 0.9598605036735535}, {"label": "NEU", "score": 0.9423457980155945}, {"label": "NEU", "score": 0.6294226050376892}, {"label": "NEU", "score": 0.9676058888435364}, {"label": "NEU", "score": 0.871745765209198}, {"label": "NEU", "score": 0.8715516328811646}, {"label": "NEU", "score": 0.9454013109207153}, {"label": "NEU", "score": 0.8328067660331726}, {"label": "NEU", "score": 0.9576826095581055}, {"label": "POS", "score": 0.8782106041908264}, {"label": "NEU", "score": 0.9202526211738586}]
[{"label": "NEU", "score": 0.9671536087989807}, {"label": "POS", "score": 0.7852944731712341}, {"label": "POS", "score": 0.5353995561599731}, {"label": "NEU", "score": 0.908729076385498}, {"label": "NEU", "score": 0.9616942405700684}, {"label": "NEU", "score": 0.9429565072059631}, {"label": "NEU", "score": 0.881543755531311}, {"label": "NEU", "score": 0.9463964104652405}, {"label": "NEU", "score": 0.7376289963722229}, {"label": "NEU", "score": 0.9351845383644104}]
.
.
.
```