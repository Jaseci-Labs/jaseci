from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

from fastapi import FastAPI
from pydantic import BaseModel

LANGUAGE = "english"
# url = "https://en.wikipedia.org/wiki/Automatic_summarization"
# SENTENCES_COUNT = 10

class ScraperModel(BaseModel):
    url: str
    sentence_count: int

app = FastAPI()

@app.post('/scraper')
def scraper(data: ScraperModel):
    SENTENCES_COUNT = data.sentence_count
    url = data.url

    sentences = []
    
    parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))

    stemmer = Stemmer(LANGUAGE)

    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    for sentence in summarizer(parser.document, SENTENCES_COUNT):
        sentences.append(str(sentence))

    return sentences