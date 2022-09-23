from turtle import xcor
from torchvision import datasets, transforms
import pandas as pd
import torch
import os


from .base import BaseDataLoader


class MnistDataLoader(BaseDataLoader):
    def __init__(self, data_dir, batch_size, shuffle=True, validation_split=0.0, num_workers=1, training=True):
        trsfm = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.1307,), (0.3081,))
        ])
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)
        self.dataset = datasets.MNIST(
            self.data_dir, train=training, download=True, transform=trsfm)
        super().__init__(self.dataset, batch_size, shuffle, validation_split, num_workers)


class SnipsDataLoader(BaseDataLoader):
    def __init__(self, data_dir, batch_size, shuffle=True, validation_split=0.0, num_workers=1, training=True):
        self.data_dir = data_dir
        df = pd.read_json(os.path.join(self.data_dir, 'SNIPS_INTENTS', 'raw', 'train.json'))
        self.dataset = SnipsDataset(df)
        super().__init__(self.dataset, batch_size, shuffle, validation_split, num_workers)


class SnipsDataset(torch.utils.data.Dataset):
    def __init__(self, df):
        self.df = df
        x = self.df['input_ids']
        y = self.df['label']
        self.x = torch.tensor(x)
        self.y = torch.tensor(y)
        # self.y = torch.nn.functional.one_hot(self.y, num_classes=10)

    def __len__(self):
        return len(self.y)

    def __getitem__(self, idx):
        return self.x[idx], self.y[idx]
