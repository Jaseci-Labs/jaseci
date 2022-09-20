from typing import Dict
import torch.nn as nn
import torch.nn.functional as F

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


class MnistModel(BaseModel):
    def __init__(self, num_classes=10):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 10, kernel_size=5)
        self.conv2 = nn.Conv2d(10, 20, kernel_size=5)
        self.conv2_drop = nn.Dropout2d()
        self.fc1 = nn.Linear(320, 50)
        self.fc2 = nn.Linear(50, num_classes)

    def forward(self, x):
        x = F.relu(F.max_pool2d(self.conv1(x), 2))
        x = F.relu(F.max_pool2d(self.conv2_drop(self.conv2(x)), 2))
        x = x.view(-1, 320)
        x = F.relu(self.fc1(x))
        x = F.dropout(x, training=self.training)
        x = self.fc2(x)
        return F.log_softmax(x, dim=1)
