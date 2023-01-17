import importlib
import pandas as pd
import torch


from .base import BaseDataLoader


class SnipsDataLoader(BaseDataLoader):
    def __init__(
        self, train_json, batch_size, shuffle=True, validation_split=0.0, num_workers=1
    ):
        df = pd.read_json(train_json)
        self.dataset = SnipsDataset(df)
        super().__init__(
            self.dataset, batch_size, shuffle, validation_split, num_workers
        )


class SnipsDataset(torch.utils.data.Dataset):
    def __init__(self, df):
        self.df = df
        x = self.df["input_ids"]
        y = self.df["label"]
        self.x = torch.tensor(x)
        self.y = torch.tensor(y)

    def __len__(self):
        return len(self.y)

    def __getitem__(self, idx):
        return self.x[idx], self.y[idx]


class CustomDataLoader(BaseDataLoader):
    def __init__(
        self, batch_size, shuffle=True, validation_split=0.0, num_workers=1, **kwargs
    ):
        # import the python file
        spec = importlib.util.spec_from_file_location("module.name", "heads/custom.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        # get the model
        self.dataset = getattr(module, "CustomDataset")(**kwargs)
        super().__init__(
            self.dataset, batch_size, shuffle, validation_split, num_workers
        )
