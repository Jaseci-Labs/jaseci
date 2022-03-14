from fastapi import HTTPException
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import en_core_web_sm as english_model
from jaseci.actions.live_actions import jaseci_action
from enum import Enum

# loading segmentation model from hugging face
tokenizer = AutoTokenizer.from_pretrained("dennlinger/roberta-cls-consec")
model = AutoModelForSequenceClassification.from_pretrained(
    "dennlinger/roberta-cls-consec")
# loading space model for sentence tokenization
spacy = english_model.load()


def segmentation(text, threshold=0.7):
    # spliting the raw test into sentences
    doc = spacy(text)
    sentences = [sent.text.strip() for sent in doc.sents]
    index = 0
    sub_segments = []
    sub_seg_index = 0
    segments = []
    for sent_ind in range(1, len(sentences)):
        # create sentence pair to evaluate
        pair = sentences[index]+" "+sentences[sent_ind]
        inputs = tokenizer.encode_plus(
            pair, max_length=128, pad_to_max_length=True, return_tensors="pt")
        outputs = model(**inputs).logits
        # getting the similarity score between sentences
        value = torch.softmax(outputs, dim=1).tolist()[0][1]
        # creating sub-segment of similar text
        if value > threshold:
            if sub_seg_index == 0:
                sub_segments.append(sentences[index])
                sub_segments.append(sentences[sent_ind])
                sub_seg_index = 1
            else:
                sub_segments.append(sentences[sent_ind])
        else:
            if not sub_segments:
                sub_segments.append(sentences[index])
            segments.append(" ".join(sub_segments))
            sub_segments = []
            sub_seg_index = 0
        index += 1
        # print(f"{index} : {value}")
    if sub_segments:
        segments.append(" ".join(sub_segments))
    # returning final segments of text
    return(segments)


@jaseci_action(act_group=['text_segmentor'])
def get_segements(text: str, threshold: float = 0.7):
    try:
        segmented_text = segmentation(text=text, threshold=threshold)
        return segmented_text
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@jaseci_action(act_group=['text_segmentor'])
def load_model(model_name: str):  # modelname could be ("wiki", "legal")
    global model, tokenizer
    if model_name == "wiki":
        tokenizer = AutoTokenizer.from_pretrained(
            "dennlinger/bert-wiki-paragraphs")
        model = AutoModelForSequenceClassification.from_pretrained(
            "dennlinger/bert-wiki-paragraphs")
    elif model_name == "legal":
        tokenizer = AutoTokenizer.from_pretrained(
            "dennlinger/roberta-cls-consec")
        model = AutoModelForSequenceClassification.from_pretrained(
            "dennlinger/roberta-cls-consec")
    else:
        raise HTTPException(status_code=500, detail="Invalid model name.")
    return f"[Model Loaded] : {model_name}"


if __name__ == '__main__':
    from jaseci.actions.remote_actions import launch_server
    print('Text Segmentor up and running')
    launch_server(port=8000)
