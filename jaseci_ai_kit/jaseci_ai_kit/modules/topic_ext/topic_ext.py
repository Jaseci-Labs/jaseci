import pandas as pd

from jaseci.actions.live_actions import jaseci_action
from jaseci.actions.remote_actions import launch_server
from fastapi import HTTPException

from .action_utils import c_tf_idf, extract_top_n_words_per_topic


@jaseci_action(act_group=["topic_ext"], allow_remote=True)
def topic_extraction(texts: list, classes: list, n_topics=5):
    try:
        doc_label_dict = {"document": texts, "label": classes}
        doc_label_df = pd.DataFrame(doc_label_dict)

        document_table = doc_label_df.groupby(["label"], as_index=False).agg(
            {"document": " ".join}
        )
        tf_idf, count = c_tf_idf(document_table.document.values, m=len(texts))

        return extract_top_n_words_per_topic(
            tf_idf=tf_idf, count=count, docs_per_topic=document_table, n=n_topics
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    print("The topic extraction module is up and running.")
    launch_server(port=8000)
