import numpy as np
import tensorflow_hub as hub
import tensorflow as tf
import tensorflow_text  # noqa
from jaseci.actions.live_actions import jaseci_action
from typing import Union


module = hub.load(
    'https://tfhub.dev/google/universal-sentence-encoder-multilingual-qa/3')


@jaseci_action(act_group=['use'], aliases=['enc_question'], allow_remote=True)
def question_encode(question: Union[str, list]):
    if(isinstance(question, list)):
        return module.signatures['question_encoder'](
            tf.constant(question))['outputs'].numpy().tolist()
    elif (isinstance(question, str)):
        return module.signatures['question_encoder'](
            tf.constant([question]))['outputs'].numpy().tolist()


@jaseci_action(act_group=['use'], aliases=['enc_answer'], allow_remote=True)
def answer_encode(answer: Union[str, list], context: Union[str, list] = None):
    if(context is None):
        context = answer
    if(isinstance(answer, list)):
        return module.signatures['response_encoder'](
            input=tf.constant(answer),
            context=tf.constant(context))['outputs'].numpy().tolist()
    elif(isinstance(answer, str)):
        return module.signatures['response_encoder'](
            input=tf.constant([answer]),
            context=tf.constant([context]))['outputs'].numpy().tolist()


@jaseci_action(act_group=['use'], allow_remote=True)
def cos_sim_score(q_emb: list, a_emb: list):
    norm = np.linalg.norm
    return np.dot(q_emb, a_emb)/(norm(q_emb)*norm(a_emb))


@jaseci_action(act_group=['use'], aliases=['qa_score'], allow_remote=True)
def dist_score(q_emb: list, a_emb: list):
    return np.inner(q_emb, a_emb).tolist()


if __name__ == "__main__":
    from jaseci.actions.remote_actions import launch_server
    launch_server(port=8000)
