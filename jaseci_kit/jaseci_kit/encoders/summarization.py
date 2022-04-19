import re
from http.client import HTTPException
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from jaseci.actions.live_actions import jaseci_action
import nltk
from sumz_utils import get_summary
nltk.download('punkt')
nltk.download('stopwords')
# default summarizer_type initailization
summarizer_type = LsaSummarizer()


@ jaseci_action(act_group=['sumz'], allow_remote=True)
def summarize(text: str, sent_count: int):
    # Tokenize text using the parser from sumy
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    # Summarize the document with sent_count sentences
    summary_text = []
    summary = summarizer_type(parser.document, sent_count)
    # get all the sentences produced by the summarizer
    for sentence in summary:
        summary_text.append(str(sentence))
    return summary_text


@ jaseci_action(act_group=['sumz'], allow_remote=True)
def config_sumz(summarizer: str = "'LexRankSummarizer', 'LsaSummarizer', 'LuhnSummarizer'"):  # noqa
    global summarizer_type
    # initialized the summarizer_type
    if summarizer in 'LuhnSummarizer':
        summarizer_type = LuhnSummarizer()
    elif summarizer in 'LsaSummarizer':
        summarizer_type = LsaSummarizer()
    elif summarizer in 'LexRankSummarizer':
        summarizer_type = LexRankSummarizer()
    else:
        raise HTTPException(status_code=404, detail=str(
            """Supported type of summarizers are
             LexRankSummarizer / LsaSummarizer / LuhnSummarizer."""))
    return f"{summarizer} summarizers initialized successfully."


@ jaseci_action(act_group=['sumz'], allow_remote=True)
def summarize_nltk_basic(text: str,  sent_count: int):
    # Removing Square Brackets and Extra Spaces
    article_text = re.sub(r'\[[0-9]*\]', ' ', text)
    article_text = re.sub(r'\s+', ' ', text)
    # Removing special characters and digits
    formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text)
    formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)
    sentence_list = nltk.sent_tokenize(article_text)
    stopwords = nltk.corpus.stopwords.words('english')

    word_frequencies = {}
    for word in nltk.word_tokenize(formatted_article_text):
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1
    maximum_frequncy = max(word_frequencies.values())

    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)
    sentence_scores = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]
    # Storing sentences into our summary.
    import heapq
    summary_sentences = heapq.nlargest(
        sent_count, sentence_scores, key=sentence_scores.get)
    return summary_sentences


@ jaseci_action(act_group=['sumz'], allow_remote=True)
def summarize_nltk_pgrnk(text: str,  sent_count: int):
    return get_summary(text=text, sent_count=sent_count)


if __name__ == "__main__":
    from jaseci.actions.remote_actions import launch_server
    launch_server(port=8000)
