# Common import of AI service
from flask import request
from base.ai_serving_base import AIServiceBase, FlaskError

# TODO: Import for this specific service
# For example, for USE
# import numpy as np
# import tensorflow_hub as hub
# import tensorflow as tf
# import tensorflow_text # noqa


class JaseciAIServiceBase():
    # TODO: Load pre-trained model and other setup
    # For example for USE
    # module = hub.load('/models/use')

    # TODO: Add API functions
    def inference(self, input):
        """
        Function that will be converted to an API endpoint via Flask.
        For example, for USE
            def encode(self, text):
                if(isinstance(text, str)):
                    text = [text]
                return self.module(text).numpy().tolist()
        """
        pass

JaseciAIService = JaseciAIServiceBase()
JaseciAIServiceApp = AIServiceBase(name='JaseciAIService')

@JaseciAIServiceApp.app.route('/JaseciAIService/', methods=['POST'])
def __router__():
    print(request.json)
    if 'op' not in request.json:
        raise FlaskError(
                message='Required param \'op\' is missing from the request.',
                status_code=404
        )
    op = request.json['op']
    
    # TODO: Map op code to function
    # For example for USE:
    # if op == 'encode':
    #     return \
    #         {'encoded': USE.encode(request.json['text'])}

    raise FlaskError(
            message='Invalid param op. ' +
                    'Supported: ecnode',
            status_code=404, payload={'original_op': request.json['op']}
    )


if __name__ == '__main__':
    print('JaseciAIService up and running')
    JaseciAIService.run(port=4673)
