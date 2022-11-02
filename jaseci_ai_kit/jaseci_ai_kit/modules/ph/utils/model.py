import importlib.util
import torch.nn as nn
import torch.nn.functional as F

from .base import BaseModel

import warnings

warnings.filterwarnings("ignore")


class PersonalizedHead(BaseModel):
    def __init__(
        self, embedding_length, ph_nhead, ph_ff_dim, batch_first, ph_nlayers, n_classes
    ):
        super().__init__()
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=embedding_length,
            nhead=ph_nhead,
            dim_feedforward=ph_ff_dim,
            batch_first=batch_first,
        )
        self.encoder = nn.TransformerEncoder(
            encoder_layer=encoder_layer, num_layers=ph_nlayers
        )
        self.decoder = nn.Linear(embedding_length, n_classes)
        nn.init.xavier_uniform_(self.decoder.weight)

    def forward(self, emb):
        x = self.encoder(emb)
        x = self.decoder(x)
        x = F.log_softmax(x, dim=-1)
        return x.squeeze(1)


class CustomModel(BaseModel):
    def __init__(self, python_file: str, module_name: str, **kwargs):
        super().__init__()
        # import the python file
        spec = importlib.util.spec_from_file_location("module.name", python_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        # get the model
        self.model = getattr(module, module_name)(**kwargs)

    def forward(self, x):
        x = self.model(x)
        return x
