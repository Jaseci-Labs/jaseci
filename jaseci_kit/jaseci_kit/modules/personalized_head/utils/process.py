import torch
from transformers import AutoTokenizer, AutoModel


class PostProcessor:
    def __init__(self):
        None

    def process(self, output):
        # output = torch.argmax(output, dim=1)
        return output


class PreProcessor:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
        self.model = AutoModel.from_pretrained("bert-base-uncased")

    def process(self, input):
        input = self.tokenizer(input, return_tensors="pt")
        emb = self.model(**input)
        emb = emb[0][:, 0, :]
        return emb
