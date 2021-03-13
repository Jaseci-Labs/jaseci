from flask import request

from base.ai_serving_base import AIServiceBase, FlaskError

import numpy as np
import tensorflow_hub as hub
import tensorflow as tf
import tensorflow_text # noqa


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

    def qa_score(self, q, a):
        return np.inner(q, a).tolist()


USE = USEBase()
USEApp = AIServiceBase(name='use')


@USEApp.app.route('/use/', methods=['POST'])
def __router__():
    if 'op' not in request.json:
        raise FlaskError(
                message='Required param \'op\' is missing from the request.',
                status_code=404
        )
    op = request.json['op']
    if op == 'encode_question':
        return \
            {'encoded': USE.question_encode(request.json['text'])}

    if op == 'encode_answer':
        context = request.json.get('context', None)
        return {'encoded': USE.answer_encode(request.json['text'],
                                             context=context)}

    if op == 'dist_score':
        return \
            {'score': USE.qa_score(request.json['encoding'][0],
                                   request.json['encoding'][1])}

    raise FlaskError(
            message='Invalid param op. ' +
                    'Supported: ecnode_question,encode_answer,dist_score',
            status_code=404, payload={'original_op': request.json['op']}
    )


if __name__ == '__main__':
    USEApp.run(port=4672)
    USEApp.log('INFO', 'USE service up and running')
