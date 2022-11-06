

#  Use  Encoder  


`use_enc` module uses the universal sentence encoder to generate sentence level embeddings.
The sentence level embeddings can then be used to calculate the similarity between two given text via cosine similarity and/or dot product.


```
actions load module jaseci_ai_kit.use_enc
```
Running ``` actions list ```  will show the new modules loaded.

`use_enc` module uses the universal sentence encoder to generate sentence level embeddings.
The sentence level embeddings can then be used to calculate the similarity between two given text via cosine similarity and/or dot product.

* `encode`: encodes the text and returns a embedding of 512 length
    * Alternate name: `get_embedding`
    * Input:
        * `text` (string or list of strings): text to be encoded
    * Return: Encoded embeddings
* `cos_sim_score`:
    * Input:
        * `q_emb` (string or list of strings): first text to be embeded
        * `a_emb` (string or list of strings): second text to be embedded
    * Return: cosine similarity score
* `text_simliarity`: calculate the simlarity score between given texts
    * Input:
        * `text1` (string): first text
        * `text2` (string): second text
    * Return: cosine similarity score
* `text_classify`: use USE encoder as a classifier
    * Input:
        * `text` (string): text to classify
        * `classes` (list of strings): candidate classification classes

#### Example Jac Usage:
```jac
# Use USE encoder for zero-shot intent classification
walker use_enc_example {
    can use.encode, use.cos_sim_score;
    has text = "What is the weather tomorrow?";
    has candidates = [
        "weather forecast",
        "ask for direction",
        "order food"
    ];
    text_emb = use.encode(text)[0];
    cand_embs = use.encode(candidates); # use.encode handles string/list

    max_score = 0;
    max_cand = 0;
    cand_idx = 0;
    for cand_emb in cand_embs {
        cos_score = use.cos_sim_score()
        if (cos_score > max_score) {
            max_score = cos_score
            max_cand = cand_idx;
        }
        cand_idx += 1;
    }

    predicted_cand = candidates[max_cand];
}
```