# Find Semantically Similar Sentences

Semantic similarity of two sentences is a measure of how closely related their meanings are. It involves comparing the underlying semantic representations of the sentences to determine the degree of overlap or similarity between them. This is typically done using techniques from natural language processing (NLP), such as word embeddings or semantic networks. The resulting similarity score can be used in various applications, such as text classification, question answering, or information retrieval, to identify relevant and related content. A high semantic similarity score suggests that the two sentences convey similar ideas, while a low score indicates that they are dissimilar.


- [Find Semantically Similar Sentences](#find-semantically-similar-sentences)
  - [Creating a walker to detect semantically two similar phrases](#creating-a-walker-to-detect-semantically-two-similar-phrases)
  - [Wrapping things together with init walker](#wrapping-things-together-with-init-walker)
  - [Executing the code](#executing-the-code)

## Creating a walker to detect semantically two similar phrases

In this section also we will be using the movie script graph which we build for previouse sections. So create a new jac file and import the `build_graph.jac` into it.

```jac
import {*} with './build_graph.jac';
```
Now let's create a walker to detect semantically similar two text phrases. We are using `sbert` encoder from `jac_nlp.sbert` module in Jaseci (to view more information about `sbert` goto [here](../../../../jaseci/jaseci_ai_kit/jac_nlp/jac_nlp/sbert/README.md) to get embeddings for the given sentence and `vector.cosine_sim` standard action to get the similarity value of two encoded sentences. we are using the dialogue from each actor in a scene to demonstrate this task. The dialogues come in as a list (observe the `movie_data.json` to understand this). We are feeding all the sentences in the dialogue as one phrase to make this simple.

```jac
walker find_similar_sentences{

    can use.encode;
    can vector.cosine_sim;

    can sbert_sim.load_model;
    can sbert_sim.getembeddings;
    can vector.cosine_sim;

    has dialogue_1;
    has dialogue_2;
    has sim_value;

    sbert_sim.load_model();

    phrase_1 = "";
    for lot in dialogue_1:
        phrase_1 = phrase_1 + ' ' + lot;

    phrase_2 = "";
    for lot in dialogue_2:
        phrase_2 = phrase_2 + ' ' + lot;

    encode1 = sbert_sim.getembeddings(phrase_1);
    encode2 = sbert_sim.getembeddings(phrase_2);

    sim_value =  vector.cosine_sim(encode1,encode2);
    if sim_value >= 0.6:
    {
        std.out(sim_value);
        std.out("phrase 1 :",phrase_1);
        std.out("phrase 2 :",phrase_2);
    }
}
```
- `can sbert_sim.load_model;` and `sbert_sim.load_model();` is to import and load the default `sbert` sim model.
- `can sbert_sim.getembeddings` is to import the embedding action,
- `can vector.cosine_sim` is to import the cosine similarity action,
- We need to compare two dialogues, so we are initializing two variables as `dialogue_1` and `dialogue_2`.
- As mentioned earlier, dialogues come as a list object, so we are converting them into phrases using simple `for` loop logic.
- `encode1 = sbert_sim.getembeddings(phrase_1)` and `encode2 = sbert_sim.getembeddings(phrase_2)` to get embeddings for `pharase_1` and `pharase_2` respectively.
- `sim_value =  vector.cosine_sim(encode1,encode2)` is to get the similarity score for the two text phrases.
- Later, we are defining a threshold value as 0.6, so the sentence pairs that exceed the threshold value are considered similar phrases.

## Wrapping things together with init walker

We are going to spawn the walke we created to compare two sentences from the `init` walker.

```
walker init{
    has _list;
    has sim_value;

    root{
         spawn here walker::build_graph;
         take-->;
    }

    location{
        take-->;
    }

    scene{
        childrens = -->node::actor;

        if childrens.length > 1:
        {
            _list = childrens.dialogue;
            pairslist = _list.list::pairwise;
            for item in pairslist:
                spawn here walker::find_similar_sentences(dialogue_1=item[0], dialogue_2=item[1]);
        }
        take -->;
    }
}
```
The attributes of actor nodes that are linked to scene nodes are dialogues.

- `childrens = -->node::actor` is to get all actor nodes attached to each scene node.
- `_list = childrens.dialogue` retrieving only the dialogue attribute from the actor nodes.
- `pairslist = _list.list::pairwise` we are making successive overlapping pairs taken from the dialogue list.
- `for item in pairslist:` this for loop calls the `find_similar_sentences` calls for the each pair in the list.

## Executing the code

Save all of these code in a `jac` file. You have to first load the `use.enc` action module before executing this code.

```
actions load module jac_nlp.sbert
jac run text_similarity.jac
```
If everything works fine you will see an output similar to this.

```
[0.7407874502901258]
phrase 1 :  Darcy, when you're done, take the soil samples to Professor Meyers in geology. Remind him, he owes me. "We?"� You know what wouon the ground. 4th BLUEld be really useful? Do you still have that friend at LIGO? Could you call in a favor? If I'm right, their observatory must have picked up
gravitational waves during last night's event. Meaning these anomalies might signify something bigger. I think the lensing around the edges is characteristic of an Einstein-Rosen Bridge. She was the only applicant. (TO DARCY) A wormhole. 4th BLUE REVISIONS 03-26-10 41B. Selvig ld be really useful? Do
looks skeptical. Jane prints out a frame-grab off the monitor. JANE (CONT'D) Erik, look... 4th BLUE REVISIONS 03-26-10 42. Jane indicates ting last night's event.he print-out showing the constellations seen through the "bubble"� in the clouds. JANE (CONT'D) What do you see here? Yes. But not our star. She was the only appls. She spreads out a STAR CHART, barely able to contain her excitement. JANE (CONT'D) This is the star alignment for our quadrant, this timCONT'D) Erik, look... 4e of year. So unless Ursa Minor decided to take the day off... those are someone else's constellations. Selvig's intrigued, in spite of him'D) What do you see herself. Darcy pulls another frame-grab of the Bifrost footage from the printer and hangs it on the wall, when something in the image catches r our quadrant, this ti
her eye. I think I left something at the hospital. As Jane walks away, we REVEAL the photo. Inside the Bifrost funnel cloud is a FIGURE -- mself. Darcy pulls anot
the vague, but unmistakable shape of a MAN.                                                                                                t something at the hosp
phrase 2 :  We might want to perform a spectral analysis. I flew all the way out here -- might as well make myself useful. This is the offer Jane's been waiting for. She gets up, inserts the piece of equipment she's been working on into a rack-mounted server. She was more than r Jane's been waiting f
a friend. You don't think this was just a magnetic storm? 4th BLUE REVISIONS 03-26-10 41A. Meaning? Jane heads over to a computer monitor. nk this was just a magn
Selvig follows. How "big"� are we talking about? Jane indicates the footage on the monitor. As the last of the Bifrost cloud disappears intt? Jane indicates the fo the night sky, there appears to be a blister in space, bulging out in convex and covered with stars. I thought you were a science major. in convex and covered w
(TO DARCY) An Einstein-Rosen Bridge -- a "theoretical"� connection between two different points of space-time. Darcy stares blankly. Stars.nts of space-time. Darc Is that...?
```