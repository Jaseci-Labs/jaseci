from django.apps import AppConfig
import numpy as np
import tensorflow_hub as hub
import tensorflow as tf
import tensorflow_text  # noqa


class USEBase():
    module = hub.load('/models/use')

    def question_encode(self, q):
        if(isinstance(q, list)):
            return self.module.signatures['question_encoder'](
                tf.constant(q))['outputs'].numpy().tolist()
        elif (isinstance(q, str)):
            return self.module.signatures['question_encoder'](
                tf.constant([q]))['outputs'].numpy().tolist()

    def answer_encode(self, a, context=None):
        if(context is None):
            context = a
        if(isinstance(a, list)):
            return self.module.signatures['response_encoder'](
                input=tf.constant(a),
                context=tf.constant(context))['outputs'].numpy().tolist()
        elif(isinstance(a, str)):
            return self.module.signatures['response_encoder'](
                input=tf.constant([a]),
                context=tf.constant([context]))['outputs'].numpy().tolist()

    def dist_score(self, q, a):
        return np.inner(q, a).tolist()


class JacApiConfig(AppConfig):
    name = 'jac_api'
    USE = USEBase()
