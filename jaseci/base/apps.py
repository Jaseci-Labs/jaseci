import tensorflow_text
import numpy as np
import tensorflow_hub as hub
import tensorflow as tf
from django.apps import AppConfig


class CoreApiConfig(AppConfig):
    name = 'base'

    class USEBase():
        module = hub.load(
            'https://tfhub.dev/google/universal-sentence-encoder-multilingual-qa/3')

        def use_question_encode(self, q):
            if(isinstance(q, list)):
                return self.module.signatures['question_encoder'](tf.constant(q))
            elif (isinstance(q, str)):
                return self.module.signatures['question_encoder'](tf.constant([q]))

        def use_answer_encode(self, a, context=None):
            if(context is None):
                context = a
            if(isinstance(a, list)):
                return self.module.signatures['response_encoder'](
                    input=tf.constant(a),
                    context=tf.constant(context))
            elif(isinstance(a, str)):
                return self.module.signatures['response_encoder'](
                    input=tf.constant([a]),
                    context=tf.constant([context]))

        def use_qa_dot(self, q, a):
            print(q, a)
            # return np.inner(question_embeddings['outputs'], response_embeddings['outputs'])
    USE = USEBase()
