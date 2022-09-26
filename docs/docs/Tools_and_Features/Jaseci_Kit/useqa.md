
# Use QA 
`use_qa` module uses the multilingual-qa to generate sentence level embeddings.
The sentence level embeddings can then be used to calculate best match between question and available answers via cosine similarity and/or dist_score.


To load the Question and Answer Module run :

```
actions load module jaseci_ai_kit.use_qa
```

* `question_encode`: encodes question and returns a embedding of 512 length
    * Alternate name: `enc_question`
    * Input:
        * `text` (string or list of strings): question to be encoded
    * Return: Encoded embeddings
* `answer_encode`: encodes answers and returns a embedding of 512 length
    * Alternate name: `enc_answer`
    * Input:
        * `text` (string or list of strings): question to be encoded
        * `context` (string or list of strings): usually the text around the answer text, for example it could be 2 sentences before plus 2 sentences after.
    * Return: Encoded embeddings
* `cos_sim_score`:
    * Input:
        * `q_emb` (string or list of strings): first embeded text
        * `a_emb` (string or list of strings): second embeded text
    * Return: cosine similarity score

* `dist_score`:
    * Input:
        * `q_emb` (string or list of strings): first embeded text
        * `a_emb` (string or list of strings): second embeded text
    * Return: inner product score
* `question_similarity`: calculate the simlarity score between given questions
    * Input:
        * `text1` (string): first text
        * `text2` (string): second text
    * Return: cosine similarity score
* `question_classify`: use USE QA as question classifier
    * Input:
        * `text` (string): text to classify
        * `classes` (list of strings): candidate classification classes
* `answer_similarity`: calculate the simlarity score between given answer
    * Input:
        * `text1` (string): first text
        * `text2` (string): second text
    * Return: cosine similarity score
* `answer_classify`: use USE encoder as answer classifier
    * Input:
        * `text` (string): text to classify
        * `classes` (list of strings): candidate classification classes
* `qa_similarity`: calculate the simlarity score between question and answer
    * Input:
        * `text1` (string): first text
        * `text2` (string): second text
    * Return: cosine similarity score
* `qa_classify`: use USE encoder as a QA classifier
    * Input:
        * `text` (string): text to classify
        * `classes` (list of strings): candidate classification classes
    * Returns: 
#### Example Jac Usage:
```jac
# Use USE_QA model for zero-shot text classification
walker use_qa_example {
    can use.qa_similarity;
    has questions = "What is your age?";
    has responses = ["I am 20 years old.", "good morning"];
    has response_contexts = ["I will be 21 next year.", "great day."];

    max_score = 0;
    max_cand = 0;
    cand_idx = 0;
    for response in responses {
        cos_score = use.qa_similarity(text1=questions,text2=response);
        std.out(cos_score);
        if (cos_score > max_score) {
            max_score = cos_score;
            max_cand = cand_idx;
        }
        cand_idx += 1;
    }

    predicted_cand = responses[max_cand];
}
```
