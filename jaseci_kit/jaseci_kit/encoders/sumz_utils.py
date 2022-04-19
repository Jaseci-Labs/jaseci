# flake8: noqa
import networkx as nx
import numpy as np
import nltk
from nltk.cluster.util import cosine_distance
try:
    from nltk.corpus import stopwords
except:
    import nltk
    nltk.download('stopwords')
finally:
    from nltk.corpus import stopwords

# constants
sw = list(set(stopwords.words('english')))
punct = [
    '!', '#', '$', '%', '&', '(', ')', '*',
    '+', ',', '-', '/', ':', ';', '<', '=', '>', '@',
    '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~'
]

book = """There was once a king of Scotland whose name was Robert Bruce. He needed to be both brave and wise because the times in which he lived were wild and rude. The King of England was at war with him and had led a great army into Scotland to drive him out of the land. Battle after battle had been fought. Six times Bruce had led his brave little army against his foes and six times his men had been beaten and driven into flight. At last his army was scattered, and he was forced to hide in the woods and in lonely places among the mountains. One rainy day, Bruce lay on the ground under a crude shed listening to the patter of the drops on the roof above him. He was tired and unhappy. He was ready to give up all hope. It seemed to him that there was no use for him to try to do anything more. As he lay thinking, he saw a spider over his head making ready to weave her web. He watched her as she toiled slowly and with great care. Six times she tried to throw her frail thread from one beam to another, and six times it fell short. “Poor thing,” said Bruce: “you, too, know what it is to fail.” But the spider did not lose hope with the sixth failure. With still more care, she made ready to try for the seventh time. Bruce almost forgot his own troubles as he watched her swing herself out upon the slender line. Would she fail again? No! The thread was carried safely to the beam and fastened there."""


def clean_text(text, sw=sw, punct=punct):
    '''
    This function will clean the input text by lowering, removing certain punctuations, stopwords and 
    new line tags.

    params:
        text (String) : The body of text you want to clean
        sw (List) : The list of stopwords you wish to removed from the input text
        punct (List) : The slist of punctuations you wish to remove from the input text

    returns:
        This function will return the input text after it's cleaned (the output will be a string) and 
        a dictionary mapping of the original sentences with its index
    '''
    article = text.lower()

    # clean punctuations
    for pun in punct:
        article = article.replace(pun, '')

    article = article.replace(
        "[^a-zA-Z]", " ").replace('\r\n', ' ').replace('\n', ' ')
    original_text_mapping = {k: v for k, v in enumerate(article.split('. '))}

    article = article.split(' ')

    # clean stopwords
    article = [x.lstrip().rstrip() for x in article if x not in sw]
    article = [x for x in article if x]
    article = ' '.join(article)

    return original_text_mapping, article


def calculate_sentence_similarity(sentence1, sentence2):
    words1 = [word for word in nltk.word_tokenize(sentence1)]
    words2 = [word for word in nltk.word_tokenize(sentence2)]

    # get uniqes words insted of a repeated words

    all_words = list(set(words1 + words2))
    # get a zeros vector / Needed for Mathematical calculation
    #                                   also we need to convert the words to a mathematical forms so we can apply the
    #                                   equation.
    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)

    # to convert text to number we will use the "Bag of words" techniqe
    for word in words1:
        # print(word)
        vector1[all_words.index(word)] += 1

    for word in words2:
        vector2[all_words.index(word)] += 1

    # print(vector2)
    return 1 - cosine_distance(vector1, vector2)


def create_similarity_matrix(sentences):
    '''
    The purpose of this function will be to create an N x N similarity matrix.
    N represents the number of sentences and the similarity of a pair of sentences
    will be determined through the Jaro-Winkler Score.

    params:
        sentences (List -> String) : This is a list of strings you want to create
                                     the similarity matrix with.

    returns:
        This function will return a square numpy matrix
    '''

    # identify sentence similarity matrix with Jaro Winkler score
    sentence_length = len(sentences)
    sim_mat = np.zeros((sentence_length, sentence_length))

    for i in range(sentence_length):
        for j in range(sentence_length):
            if i != j:
                similarity = calculate_sentence_similarity(
                    sentences[i], sentences[j])
                sim_mat[i][j] = similarity
    return sim_mat


def get_summary(text, sent_count):
    original_text_mapping, cleaned_book = clean_text(text)

    # get sentences
    sentences = [x for x in cleaned_book.split(
        '. ') if x not in ['', ' ', '..', '.', '...']]

    sim_mat = create_similarity_matrix(sentences)

    # create network
    G = nx.from_numpy_matrix(sim_mat)

    # calculate page rank scores
    pr_sentence_similarity = nx.pagerank(G)

    ranked_sentences = [
        (original_text_mapping[sent], rank) for sent, rank in sorted(pr_sentence_similarity.items(), key=lambda item: item[1], reverse=True)
    ]
    summary = []
    for i in ranked_sentences[:sent_count]:
        summary.append(i[0])
    return summary
# print(ranked_sentences[0][0])
