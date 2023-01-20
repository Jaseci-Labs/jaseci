import os
import configparser

import numpy as np

from random import sample
from typing import List

from sklearn.feature_extraction.text import CountVectorizer
from transformers import T5ForConditionalGeneration, T5Tokenizer, pipeline

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
