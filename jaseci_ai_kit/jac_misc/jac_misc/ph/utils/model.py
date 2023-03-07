import importlib.util
import torch.nn as nn
import torch.nn.functional as F
import torch

from .base import BaseModel

import warnings

warnings.filterwarnings("ignore")


class PHClassifier(BaseModel):
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


class PHVector2Vector(BaseModel):
    def __init__(
        self,
        input_dim,
        ph_nhead,
        ph_ff_dim,
        batch_first,
        ph_nlayers,
        output_dim,
    ):
        super().__init__()
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=input_dim,
            nhead=ph_nhead,
            dim_feedforward=ph_ff_dim,
            batch_first=batch_first,
        )
        self.encoder = nn.TransformerEncoder(
            encoder_layer=encoder_layer, num_layers=ph_nlayers
        )
        self.decoder = nn.Linear(input_dim, output_dim)
        nn.init.xavier_uniform_(self.decoder.weight)

    def forward(self, emb):
        x = self.encoder(emb)
        x = self.decoder(x)
        return x


class PHVectorSimilarity(BaseModel):
    def __init__(
        self, input_dim, ph_nhead, ph_ff_dim, batch_first, ph_nlayers, output_dim
    ):
        super().__init__()
        self.input_dim = input_dim
        self.ph_v2v = PHVector2Vector(
            input_dim, ph_nhead, ph_ff_dim, batch_first, ph_nlayers, output_dim
        )

    def forward(self, emb):
        if emb.shape[1] == self.input_dim * 2:
            emb1 = emb[:, : self.input_dim]
            emb2 = emb[:, self.input_dim :]
            assert emb1.shape == emb2.shape
            x1 = self.ph_v2v(emb1)
            x2 = self.ph_v2v(emb2)
            x = torch.cat((x1, x2), dim=1)
        else:
            assert emb.shape[1] == self.input_dim
            x = self.ph_v2v(emb)
        return x


class CustomModel(BaseModel):
    def __init__(self, python_file: str = "heads/custom.py", **kwargs):
        super().__init__()
        # import the python file
        spec = importlib.util.spec_from_file_location("module.name", python_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        # get the model
        self.model = getattr(module, "CustomModel")(**kwargs)

    def forward(self, x):
        x = self.model(x)
        return x
