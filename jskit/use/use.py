import numpy as np
import tensorflow_hub as hub
import tensorflow as tf
import tensorflow_text  # noqa
import jaseci.actions.remote_actions as jra


module = hub.load(
    'https://tfhub.dev/google/universal-sentence-encoder-multilingual-qa/3')


@jra.jaseci_action()
def question_encode(q):
    if(isinstance(q, list)):
        return module.signatures['question_encoder'](
            tf.constant(q))['outputs'].numpy().tolist()
    elif (isinstance(q, str)):
        return module.signatures['question_encoder'](
            tf.constant([q]))['outputs'].numpy().tolist()


@jra.jaseci_action()
def answer_encode(a, context=None):
    if(context is None):
        context = a
    if(isinstance(a, list)):
        return module.signatures['response_encoder'](
            input=tf.constant(a),
            context=tf.constant(context))['outputs'].numpy().tolist()
    elif(isinstance(a, str)):
        return module.signatures['response_encoder'](
            input=tf.constant([a]),
            context=tf.constant([context]))['outputs'].numpy().tolist()


@jra.jaseci_action()
def cos_sim_score(q_emb, a_emb):
    norm = np.linalg.norm
    return np.dot(q_emb, a_emb)/(norm(q_emb)*norm(a_emb))
