import uuid
from typing import Dict
import torch.nn as nn

from .base import BaseModel


class PersonalizedHead(BaseModel):
    def __init__(self, config: Dict, id: str = None):
        super().__init__()
        self.id = id if id else str(uuid.uuid4())
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=config["embedding_length"],
            nhead=config["ph_nhead"],
            dim_feedforward=config["ph_ff_dim"],
            batch_first=config["batch_first"]
        )
        self.encoder = nn.TransformerEncoder(
            encoder_layer=encoder_layer, num_layers=config["ph_nlayers"]
        )
        self.decoder = nn.Linear(
            config["embedding_length"], config["n_classes"]
        )
        nn.init.xavier_uniform_(self.decoder.weight)

    def forward(self, emb):
        _, hidden_states = emb
        encoder_tensor = self.encoder(hidden_states)
        text_embedding_tensor = encoder_tensor[:, 0, :]
        scores = self.decoder(text_embedding_tensor)
        return scores

class SequentialPersonalizedHead(BaseModel):
    def __init__(self, config: Dict, id: str = None):
        super().__init__()
        self.id = id if id else str(uuid.uuid4())