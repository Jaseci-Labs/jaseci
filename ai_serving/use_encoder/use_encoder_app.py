from flask import request

from base.ai_serving_base import AIServiceBase, FlaskError

import numpy as np
import tensorflow_hub as hub
import tensorflow as tf
import tensorflow_text  # noqa


class USEEncoderBase():
    module = hub.load('/models/use')

    def encode(self, text):
        if(isinstance(text, str)):
            text = [text]
        return self.module(text).numpy().tolist()


USE = USEEncoderBase()
USEEncoderApp = AIServiceBase(name='use_encoder')


@USEEncoderApp.app.route('/use-encoder/', methods=['POST'])
def __router__():
    print(request.json)
    if 'op' not in request.json:
        raise FlaskError(
            message='Required param \'op\' is missing from the request.',
            status_code=404
        )
    op = request.json['op']
    if op == 'encode':
        return \
            {'encoded': USE.encode(request.json['text'])}

    raise FlaskError(
        message='Invalid param op. ' +
        'Supported: ecnode',
        status_code=404, payload={'original_op': request.json['op']}
    )


if __name__ == '__main__':
    print('USE encoder service up and running')
    USEEncoderApp.run(port=4673)
