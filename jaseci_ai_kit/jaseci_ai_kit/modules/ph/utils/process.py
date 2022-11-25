import torch
from transformers import AutoTokenizer, AutoModel
import importlib


class SnipsPostProcessor:
    def __init__(self, to_list: bool = False):
        self.to_list = to_list

    def process(self, output):
        output = torch.argmax(output, dim=1)
        if self.to_list:
            output = output.tolist()[0]
        return output


class SnipsPreProcessor:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
        self.model = AutoModel.from_pretrained("bert-base-uncased")

    def process(self, input):
        input = self.tokenizer(input, return_tensors="pt")
        emb = self.model(**input)
        emb = emb[0][:, 0, :]
        return emb


class V2VPostProcessor:
    def __init__(self):
        pass

    def process(self, output: torch.Tensor) -> list:
        return output.tolist()[0]


class V2VPreProcessor:
    def __init__(self):
        pass

    def process(self, input: list) -> torch.Tensor:
        input = torch.tensor(input)
        return input


class CustomProcessor:
    def __init__(
        self, module_name: str, python_file: str = "heads/custom.py", **kwargs
    ):
        spec = importlib.util.spec_from_file_location("module.name", python_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.processor = getattr(module, module_name)(**kwargs)

    def process(self, input):
        return self.processor.process(input)
