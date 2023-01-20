import warnings

import pandas as pd

from jaseci.actions.live_actions import jaseci_action
from jaseci.actions.remote_actions import launch_server
from fastapi import HTTPException

from .action_utils import c_tf_idf, extract_top_n_words_per_topic, generate_topic_label

warnings.filterwarnings("ignore")
warnings.warn("ignore")


@jaseci_action(act_group=["topic_ext"], allow_remote=True)
def topic_extraction(
    texts: list,
    classes: list,
    n_topics: int = 5,
    min_tokens: int = 1,
    max_tokens: int = 2,
):

    if min_tokens > max_tokens:
        raise ValueError(
            "The value of min_tokens shoul be less or equal than the value of max_tokens"
        )
    try:
        doc_label_dict = {"document": texts, "label": classes}
        doc_label_df = pd.DataFrame(doc_label_dict)

        document_table = doc_label_df.groupby(["label"], as_index=False).agg(
            {"document": " ".join}
        )
        tf_idf, count = c_tf_idf(
            document_table.document.values,
            m=len(texts),
            ngram_range=(min_tokens, max_tokens),
        )

        return extract_top_n_words_per_topic(
            tf_idf=tf_idf, count=count, docs_per_topic=document_table, n=n_topics
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@jaseci_action(act_group=["topic_ext"], allow_remote=True)
def headline_generation(texts: list, classes: list):
    try:
        doc_label_dict = {"document": texts, "label": classes}
        doc_label_df = pd.DataFrame(doc_label_dict)

        document_table = (
            doc_label_df.groupby("label")["document"].apply(list).reset_index()
        )
        document_table["headline"] = document_table["document"].apply(
            lambda x: generate_topic_label(x)
        )
        ret_dict = document_table.set_index("label").to_dict()["headline"]
        return ret_dict

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    print("The topic extraction module is up and running.")
    launch_server(port=8000)
