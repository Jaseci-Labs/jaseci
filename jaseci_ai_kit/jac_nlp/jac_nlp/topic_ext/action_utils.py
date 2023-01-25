import os
import configparser

import numpy as np

from random import sample
from typing import List

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import T5ForConditionalGeneration, T5Tokenizer, pipeline
from sentence_transformers import SentenceTransformer

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), "config.cfg"))


##################################################################################
#                                                                                #
#                  Model Configurations                                          #
#                                                                                #
##################################################################################

tokenizer = T5Tokenizer.from_pretrained(config["MODELS_NAMES"]["TOKENIZER"])
language_model = T5ForConditionalGeneration.from_pretrained(
    config["MODELS_NAMES"]["LANGUAGE_MODEL"]
)
headline_generator = T5ForConditionalGeneration.from_pretrained(
    config["MODELS_NAMES"]["HEADLINE_GENERATOR"]
)

sentence_embed = SentenceTransformer(config["MODELS_NAMES"]["DOCUMENT_EMBED"])

summarizer = pipeline(
    "summarization",
    model=language_model,
    tokenizer=tokenizer,
    framework="tf",
    max_length=50,
    min_length=5,
)


def c_tf_idf(documents, m, ngram_range=(1, 1)):
    """
    Calculating class based tf_idf vectors.

    Parameters:
    ------------
    documents : list of text documents.
    m : number of documents.
    ngram_range: tupple.

    Returns:

    tf_idf: calculated if_idf vectors
    count: countvectorizer object.
    """
    count = CountVectorizer(ngram_range=ngram_range, stop_words="english").fit(
        documents
    )
    t = count.transform(documents).toarray()
    w = t.sum(axis=1)
    tf = np.divide(t.T, w)
    sum_t = t.sum(axis=0)
    idf = np.log(np.divide(m, sum_t)).reshape(-1, 1)
    tf_idf = np.multiply(tf, idf)

    return tf_idf, count


def extract_top_n_words_per_topic(tf_idf, count, docs_per_topic, n=5):
    """
    Extracting top n words from each class

    Parameters:
    ------------
    tf_idf: tf-idf vectors
    count:
    docs_per_topic:
    n: number of topic expected

    Returns:
    top_n_words:  Dict,
    """
    words = count.get_feature_names_out()
    labels = list(docs_per_topic.label)
    tf_idf_transposed = tf_idf.T
    indices = tf_idf_transposed.argsort()[:, -n:]
    top_n_words = {
        label: [(words[j], tf_idf_transposed[i][j]) for j in indices[i]][::-1]
        for i, label in enumerate(labels)
    }
    return top_n_words


def generate_topic_label(documents: List[str]) -> str:
    """
    Generate summery for grouped documents in each label, and generate a headline assigined to each label.

    Parameters:
    -------------
    articles : List of Strings,

    Returns:
    -------------
    head_line: Dict, a dictio

    """

    summary_list = []
    current_token_length = 0
    max_token_length = 512

    for article in sample(documents, k=len(documents)):
        summary = summarizer(article)[0]["summary_text"]
        current_token_length += len(tokenizer.encode(summary))
        if current_token_length >= max_token_length:
            break
        summary_list.append(summary)

    encoding = tokenizer.encode(
        "headline: " + " ".join(summary_list), return_tensors="pt"
    )
    output = headline_generator.generate(encoding)
    head_line = tokenizer.decode(output[0][1:-1])

    return head_line


def mmr(input_text, top_n, n_gram_range=(1, 1), diversity=0.02):
    """
    Maximal Marginal Relevance based algorithm for extracting keywords
    """

    # Extract similarity within words, and between words and the document
    doc_embedding = sentence_embed.encode([input_text])
    count = CountVectorizer(ngram_range=n_gram_range, stop_words="english").fit(
        [input_text]
    )
    candidates = count.get_feature_names_out()
    candidate_embeddings = sentence_embed.encode(candidates)

    word_doc_similarity = cosine_similarity(candidate_embeddings, doc_embedding)
    word_similarity = cosine_similarity(candidate_embeddings)

    # Initialize candidates and already choose best keyword/keyphras
    keywords_idx = [np.argmax(word_doc_similarity)]
    candidates_idx = [i for i in range(len(candidates)) if i != keywords_idx[0]]

    for _ in range(top_n - 1):
        # Extract similarities within candidates and
        # between candidates and selected keywords/phrases
        candidate_similarities = word_doc_similarity[candidates_idx, :]
        target_similarities = np.max(
            word_similarity[candidates_idx][:, keywords_idx], axis=1
        )

        # Calculate MMR
        mmr = (
            1 - diversity
        ) * candidate_similarities - diversity * target_similarities.reshape(-1, 1)
        mmr_idx = candidates_idx[np.argmax(mmr)]

        # Update keywords & candidates
        keywords_idx.append(mmr_idx)
        candidates_idx.remove(mmr_idx)

    return [candidates[idx] for idx in keywords_idx]
