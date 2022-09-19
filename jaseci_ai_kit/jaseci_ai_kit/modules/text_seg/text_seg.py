import spacy
from fastapi import HTTPException
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from jaseci.actions.live_actions import jaseci_action

# loading segmentation model from hugging face
tokenizer = AutoTokenizer.from_pretrained("dennlinger/roberta-cls-consec")
model = AutoModelForSequenceClassification.from_pretrained(
    "dennlinger/roberta-cls-consec"
)
# Download the pretrained model pipeline
spacy.cli.download("en_core_web_sm")
# loading space model for sentence tokenization
pipeline = spacy.load("en_core_web_sm")


def segmentation(text, threshold=0.85):
    """
    This function takes the raw text, converts them into sentence tokens.
    Tokens are then provided to the sequence classifier to predict the
    syntactical similarity.
    """
    # spliting the raw test into sentences
    doc = pipeline(text)
    sentences = [sent.text.strip() for sent in doc.sents]
    index = 0
    sub_segments = []
    segments = []
    for sent_ind in range(1, len(sentences)):
        # create sentence pair to evaluate
        pair = sentences[index] + " " + sentences[sent_ind]
        inputs = tokenizer.encode_plus(
            pair, max_length=128, pad_to_max_length=True, return_tensors="pt"
        )
        outputs = model(**inputs).logits
        # getting the similarity score between sentences
        value = torch.softmax(outputs, dim=1).tolist()[0][1]
        # creating sub-segment of similar text
        if value > threshold:
            if not sub_segments:
                sub_segments.append(sentences[index])
                sub_segments.append(sentences[sent_ind])
            else:
                sub_segments.append(sentences[sent_ind])
        else:

            if not sub_segments:
                sub_segments.append(sentences[index])
            segments.append(" ".join(sub_segments))
            sub_segments = []
            sub_segments.append(sentences[sent_ind])
        index += 1
    if sub_segments:
        segments.append(" ".join(sub_segments))
    # returning final segments of text
    return segments


@jaseci_action(act_group=["text_seg"], allow_remote=True)
def get_segments(text: str, threshold: float = 0.7):
    try:
        segmented_text = segmentation(text=text, threshold=threshold)
        return segmented_text
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@jaseci_action(act_group=["text_seg"], allow_remote=True)
# NOTE: Temporary fix for jaseci kit CI pipeline.
# Need to change back to load_model for consistency with other models.
def seg_load_model(model_name: str):  # modelname could be ("wiki", "legal")
    global model, tokenizer
    if model_name == "wiki":
        tokenizer = AutoTokenizer.from_pretrained("dennlinger/bert-wiki-paragraphs")
        model = AutoModelForSequenceClassification.from_pretrained(
            "dennlinger/bert-wiki-paragraphs"
        )
    elif model_name == "legal":
        tokenizer = AutoTokenizer.from_pretrained("dennlinger/roberta-cls-consec")
        model = AutoModelForSequenceClassification.from_pretrained(
            "dennlinger/roberta-cls-consec"
        )
    else:
        raise HTTPException(status_code=500, detail="Invalid model name.")
    return f"[Model Loaded] : {model_name}"


if __name__ == "__main__":
    from jaseci.actions.remote_actions import launch_server

    print("Text Segmentor up and running")
    launch_server(port=8000)
