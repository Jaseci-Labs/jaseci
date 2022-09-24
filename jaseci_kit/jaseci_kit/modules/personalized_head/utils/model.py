from typing import Dict
import torch.nn as nn
import torch.nn.functional as F

from .base import BaseModel


class PersonalizedHead(BaseModel):
    def __init__(self, embedding_length, ph_nhead, ph_ff_dim, batch_first, ph_nlayers, n_classes):
        super().__init__()
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=embedding_length,
            nhead=ph_nhead,
            dim_feedforward=ph_ff_dim,
            batch_first=batch_first
        )
        self.encoder = nn.TransformerEncoder(
            encoder_layer=encoder_layer, num_layers=ph_nlayers
        )
        self.decoder = nn.Linear(
            embedding_length, n_classes
        )
        nn.init.xavier_uniform_(self.decoder.weight)

    def forward(self, emb):
        x = self.encoder(emb)
        x = self.decoder(x)
        x = F.log_softmax(x, dim=-1)
        return x.squeeze(1)


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
