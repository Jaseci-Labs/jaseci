import torch
import torch.nn.functional as F
from torch import nn
from transformers import AdamW
import pytorch_lightning as pl


class BiEncoder(pl.LightningModule):
    def __init__(self, *inputs, **kwargs):
        super().__init__()

        # Text embedder
        self.text_embedder = kwargs["t_model"]
        # Entity embedder
        self.entity_embedder = kwargs["e_model"]

        self.fc_text_embed = nn.Linear(kwargs["t_config"].hidden_size, 128)
        self.fc_ent_embed = nn.Linear(kwargs["e_config"].hidden_size, 128)

    def get_entity_embeddings(self, entity_inputs):
        entity_inputs["input_ids"] = entity_inputs["input_ids"].squeeze(0)
        entity_inputs["attention_mask"] = entity_inputs["attention_mask"].squeeze(0)
        ent_embed = self.entity_embedder(**entity_inputs).last_hidden_state[:, 0]
        ent_embed = self.fc_ent_embed(ent_embed)
        return ent_embed

    def get_text_embeddings(self, text_inputs):
        text_inputs["input_ids"] = text_inputs["input_ids"].squeeze(0)
        text_inputs["attention_mask"] = text_inputs["attention_mask"].squeeze(0)
        text_embed = self.text_embedder(
            text_inputs["input_ids"], text_inputs["attention_mask"]
        ).last_hidden_state[:, 0]
        text_embed = self.fc_text_embed(text_embed)
        return text_embed

    def forward(self, text_inputs, entity_inputs=None, **kwargs):
        text_embed = self.get_text_embeddings(text_inputs)
        if entity_inputs:
            ent_embed = self.get_entity_embeddings(entity_inputs)
            return text_embed, ent_embed

        return text_embed

    def training_step(self, batch=None, batch_idx=None):
        text_embed, ent_embed = self.forward(**batch)
        scores = text_embed.mm(ent_embed.t())
        bs = ent_embed.size(0)
        target = torch.LongTensor(torch.arange(bs))
        target = target.to(self.device)
        loss = F.cross_entropy(scores, target, reduction="mean")
        return loss

    def validation_step(self, batch, batch_idx):
        text_embed, ent_embed = self.forward(**batch)
        scores = text_embed.mm(ent_embed.t())
        bs = ent_embed.size(0)
        target = torch.LongTensor(torch.arange(bs))
        target = target.to(self.device)
        loss = F.cross_entropy(scores, target, reduction="mean")
        return {"val_loss": loss}

    def validation_epoch_end(self, outputs):
        avg_loss = torch.stack([x["val_loss"] for x in outputs]).mean()
        self.log("val_loss", avg_loss, prog_bar=True)

    def predict_step(self, batch, batch_idx):
        text_embed, ent_embed = self.forward(**batch)
        scores = text_embed.mm(ent_embed.t())
        return scores

    def configure_optimizers(self):
        optimizer = AdamW(self.parameters(), lr=2e-5)
        return optimizer
