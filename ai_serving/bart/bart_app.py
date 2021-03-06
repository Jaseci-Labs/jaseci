from flask import request, jsonify

from base.ai_serving_base import AIServiceBase, FlaskError

from transformers import BartForSequenceClassification, BartTokenizer


class BARTBase():

    tokenizer = BartTokenizer.from_pretrained('/bart/facebook/bart-large-mnli')
    classifier = BartForSequenceClassification.from_pretrained(
            '/bart/facebook/bart-large-mnli')

    hypothesis_prefix = "This is related to "

    def eval_assoc(self, text_in, cats):
        """
        Encode categories with BART and return the catories sorted by their
        relevance to text_in, along with the association score.
        """
        results = []
        hypothesis_prefix = "This is related to "
        for cat in cats:
            hypothesis = hypothesis_prefix + cat

            input_ids = \
                self.tokenizer.encode(text_in, hypothesis, return_tensors='pt')
            logits = self.classifier(input_ids)[0]

            entail_contradiction_logits = logits[:, [0, 2]]
            probs = entail_contradiction_logits.softmax(dim=1)
            true_prob = probs[:, 1].item()

            results.append(true_prob)

        sorted_results = \
            sorted(zip(cats, results), key=lambda x: x[1], reverse=True)
        return sorted_results


BART = BARTBase()
BARTApp = AIServiceBase(name='bart')


@BARTApp.app.errorhandler(FlaskError)
def handle_flask_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@BARTApp.app.route('/bart/', methods=['POST'])
def __router__():

    if 'op' not in request.json:
        raise FlaskError(
                message='Required param \'op\' is missing from the request.',
                status_code=404
                )
    if 'text' not in request.json or 'cats' not in request.json:
        raise FlaskError(
                message='Required param \'text\' or \'cats\' is missing.',
                status_code=404
                )

    op = request.json['op']
    if op == 'eval_assoc':
        return {
            'sorted_associations': BART.eval_assoc(
                                        text_in=request.json['text'],
                                        cats=request.json['cats'])}

    raise FlaskError(
            message='Invalid param \'op\'. Supported: \'eval_assoc\'',
            status_code=404, payload={'original_op': request.json['op']})


if __name__ == '__main__':
    BARTApp.run(port=4671)
    BARTApp.log('INFO', 'BART service up and running')
