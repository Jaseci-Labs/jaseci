import numpy as np
import tensorflow_hub as hub
import tensorflow as tf
import tensorflow_text  # noqa
import jaseci.actions.remote_actions as jra
from typing import Union


module = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")


@jra.jaseci_action(act_group=['use'], aliases=['get_embedding'])
def encode(text: Union[str, list]):
    if(isinstance(text, str)):
        text = [text]
    return module(text).numpy().tolist()


@jra.jaseci_action(act_group=['use'])
def cos_sim_score(q_emb: list, a_emb: list):
    norm = np.linalg.norm
    return np.dot(q_emb, a_emb)/(norm(q_emb)*norm(a_emb))


if __name__ == "__main__":
    jra.launch_server(port=8000)
