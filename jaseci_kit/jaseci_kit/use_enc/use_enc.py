import numpy as np
import tensorflow_hub as hub
import tensorflow as tf
import tensorflow_text  # noqa
from jaseci.actions.live_actions import jaseci_action
from typing import Union


module = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")


@jaseci_action(act_group=['use'], aliases=['get_embedding'], allow_remote=True)
def encode(text: Union[str, list]):
    if(isinstance(text, str)):
        text = [text]
    return module(text).numpy().tolist()


@jaseci_action(act_group=['use'], allow_remote=True)
def cos_sim_score(q_emb: list, a_emb: list):
    norm = np.linalg.norm
    return np.dot(q_emb, a_emb)/(norm(q_emb)*norm(a_emb))


if __name__ == "__main__":
    from jaseci.actions.remote_actions import launch_server
    launch_server(port=8000)
