import torch
from transformers import AutoTokenizer, AutoModelForMaskedLM

class PostProcessor:
    def __init__(self):
        None

    def process(self, output):
        return output

class PreProcessor:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
        self.model = AutoModelForMaskedLM.from_pretrained("bert-base-uncased")

    def process(self, input):
        input = self.tokenizer(input, return_tensors="pt")
        emb = self.model(**input)
        return emb.logits
