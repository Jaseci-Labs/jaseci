import numpy as np
import tensorflow_hub as hub
import tensorflow as tf
import tensorflow_text  # noqa
import jaseci.actions.remote_actions as jra


module = hub.load(
    'https://tfhub.dev/google/universal-sentence-encoder-multilingual-qa/3')


@jra.jaseci_action()
def question_encode(question: str):
    if(isinstance(question, list)):
        return module.signatures['question_encoder'](
            tf.constant(question))['outputs'].numpy().tolist()
    elif (isinstance(question, str)):
        return module.signatures['question_encoder'](
            tf.constant([question]))['outputs'].numpy().tolist()


@jra.jaseci_action()
def answer_encode(answer: str, context: str = None):
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


@jra.jaseci_action()
def cos_sim_score(q_emb: list, a_emb: list):
    norm = np.linalg.norm
    return np.dot(q_emb, a_emb)/(norm(q_emb)*norm(a_emb))
