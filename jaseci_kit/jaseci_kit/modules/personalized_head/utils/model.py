from typing import Dict
import torch.nn as nn

from .base import BaseModel


class PersonalizedHead(BaseModel):
    def __init__(self, config: Dict, id: str = None):
        super().__init__()
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
        encoder_tensor = self.encoder(emb)
        text_embedding_tensor = encoder_tensor[:, 0, :]
        scores = self.decoder(text_embedding_tensor)
        return scores

class Yolov4(BaseModel):
    def __init__(self, config: Dict, id: str = None):
        super().__init__()
        self.config = config
        self.id = id
        self.model = Darknet(config["cfg"], config["img_size"])
        self.model.load_state_dict(torch.load(config["weights"], map_location="cpu")["model"])
        self.model.to(self.device).eval()

    def forward(self, x):
        return self.model(x)
