from fastapi import HTTPException
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from jaseci.actions.live_actions import jaseci_action
from sumy.parsers.html import HtmlParser
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import nltk

nltk.download("punkt")
nltk.download("stopwords")

# summarizes the text / url passed to the endpoint and
# returns summary based on the sentences.


@jaseci_action(act_group=["cl_summer"], allow_remote=True)
def summarize(
    text: str = "none",
    url: str = "none",
    sent_count: int = 1,
    summarizer_type: str = "LsaSummarizer",
):

    LANGUAGE = "english"

    # checking which summarization models to use
    if summarizer_type == "LsaSummarizer":
        summarizer_type = LsaSummarizer

    elif summarizer_type == "LexRankSummarizer":
        summarizer_type = LexRankSummarizer

    elif summarizer_type == "LuhnSummarizer":
        summarizer_type = LuhnSummarizer

    else:
        raise HTTPException(
            status_code=404,
            detail=str(
                """Supported type of summarizers are
                LexRankSummarizer / LsaSummarizer / LuhnSummarizer."""
            ),
        )

    # checks if text / url key exists on the api payload
    if text != "none" and url == "none":
        parser = PlaintextParser.from_string(text, Tokenizer(LANGUAGE))
    elif text == "none" and url != "none":
        parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))
    elif text != "none" and url != "none":
        raise HTTPException(
            status_code=404,
            detail=str("only one of the following key is required text / url."),
        )
    else:
        raise HTTPException(
            status_code=404,
            detail=str("one of the following key is required text / url."),
        )

    sentences = []

    stemmer = Stemmer(LANGUAGE)
    summarizer = summarizer_type(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    for sentence in summarizer(parser.document, sent_count):
        sentences.append(str(sentence))

    return sentences


if __name__ == "__main__":
    from jaseci.actions.remote_actions import launch_server

    launch_server(port=8000)
