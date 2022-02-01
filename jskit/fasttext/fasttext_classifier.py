# Common import of AI service
from flask import request
from base.ai_serving_base import AIServiceBase, FlaskError

from .json_to_train import json_to_train, prep_sentence, label_to_intent
from .config import model_file_path, train_file_path

import fasttext
import os


class FasttextClassifierBase:
    # keeps loaded model
    model = None

    def train(self):
        print('Training...')
        json_to_train()
        model = fasttext.train_supervised(train_file_path, lr=0.25, epoch=30, wordNgrams=3)
        print('Compressing...')
        # model.quantize(input=train_file_path, retrain=True)
        print('Saving...')
        model.save_model(model_file_path)
        print('')
        print(f'Model saved to {model_file_path}.')

        labels = [label.replace('__label__', '') for label in model.labels]
        print('')
        print(f'LABELS ({len(labels)}):')
        for label in labels:
            print(f'- {label}')

        return model

    def load_model(self):
        if os.path.exists(model_file_path):
            print('Model exists. Loading...')
            self.model = fasttext.load_model(model_file_path)
            print(f'Loaded {model_file_path}')
        else:
            print('Model does not exist. Training...')
            self.model = self.train()

        return self.model

    def predict(self, sentences):
        model = self.model if self.model else self.load_model()
        result = {}
        for sentence in sentences:
            result[sentence] = []
            predictions = model.predict(prep_sentence(sentence))
            for pre in zip(predictions[0], predictions[1]):
                result[sentence].append({
                    'sentence': sentence,
                    'intent': label_to_intent(pre[0]),
                    'probability': pre[1]
                })
        return result


FasttextClassifier = FasttextClassifierBase()
FasttextClassifierApp = AIServiceBase(name='FasttextClassifier')

@FasttextClassifierApp.app.route('/fasttext-classifier/', methods=['POST'])
def __router__():
    print(request.json)
    if 'op' not in request.json:
        raise FlaskError(
                message='Required param \'op\' is missing from the request.',
                status_code=404
        )
    op = request.json['op']
    if op == 'predict':
        if 'sentences' in request.json:
            return FasttextClassifier.predict(request.json['sentences'])
        else:
            raise FlaskError(
                message='"sentences" not found in request',
                status_code=400,
                payload=request.json
            )

    raise FlaskError(
            message='Invalid param op. ' +
                    'Supported: predict',
            status_code=404, payload={'original_op': request.json['op']}
    )


if __name__ == '__main__':
    print('FasttextClassifier up and running')
    FasttextClassifier.load_model()
    FasttextClassifierApp.run(port=4675)
