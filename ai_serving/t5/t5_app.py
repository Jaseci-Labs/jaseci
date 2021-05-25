from flask import request, jsonify
import torch
from base.ai_serving_base import AIServiceBase, FlaskError
from transformers import T5Tokenizer, T5ForConditionalGeneration, T5Config


class T5Base():
    tokenizer = T5Tokenizer.from_pretrained('/t5-small/')
    model = T5ForConditionalGeneration.from_pretrained('/t5-small/')
    device = torch.device('cpu')

    def summarize(self, text_in, min_length=10, max_length=20):
        """
        Encode incoming text with t5-small model and generate a summary with 
        length between min and max
        """
        tokenized_text = self.tokenizer.encode(
            f'summarize: {text_in}', return_tensor='pt').to(device)
        
        summary_ids = self.model.generate(
            tokenized_text,
            # Number of beams for beam search. 1 means no beam search.
            num_beams=4,
            # If set to int > 0, all ngrams of that size can only occur once. 
            no_repeat_ngram_size=2,
            min_length=min_length,
            max_length=max_length,
            # Whether to stop the beam search when at least num_beams 
            # sentences are finished per batch.
            early_stopping=True
        )

        text_out = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return text_out
        
T5 = T5Base()
T5App = AIServiceBase(name='t5')

@T5App.app.errorhandler(FlaskError)
def handle_flask_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@T5App.app.route('/t5/', methods=['POST'])
def __router__():

    if 'op' not in request.json:
        raise FlaskError(
                message='Required param \'op\' is missing from the request.',
                status_code=404
                )
    if 'text' not in request.json:
        raise FlaskError(
                message='Required param \'text\' is missing.',
                status_code=404
                )

    op = request.json['op']
    if op == 'summarize':
        min_length = request.json.get('min_length', 10)
        max_length = request.json.get('max_length', 20)

        return {
            'summary': T5.summarize(
                text_in=request.json['text'],
                min_length=min_length,
                max_length=max_length)
                }

    raise FlaskError(
            message='Invalid param \'op\'. Supported: \'summarize\'',
            status_code=404, payload={'original_op': request.json['op']})


if __name__ == '__main__':
    T5App.run(port=4673)
    T5App.log('INFO', 'T5 service up and running')
