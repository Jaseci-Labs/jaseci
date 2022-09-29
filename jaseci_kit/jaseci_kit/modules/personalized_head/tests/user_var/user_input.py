import torch
from torch.nn import functional as F
from torchvision import datasets, transforms
import os
import PIL

# test model module by the user


class MnistModel(torch.nn.Module):
    def __init__(self, num_classes=10):
        super().__init__()
        self.conv1 = torch.nn.Conv2d(1, 10, kernel_size=5)
        self.conv2 = torch.nn.Conv2d(10, 20, kernel_size=5)
        self.conv2_drop = torch.nn.Dropout2d()
        self.fc1 = torch.nn.Linear(320, 50)
        self.fc2 = torch.nn.Linear(50, num_classes)

    def forward(self, x):
        x = F.relu(F.max_pool2d(self.conv1(x), 2))
        x = F.relu(F.max_pool2d(self.conv2_drop(self.conv2(x)), 2))
        x = x.view(-1, 320)
        x = F.relu(self.fc1(x))
        x = F.dropout(x, training=self.training)
        x = self.fc2(x)
        return F.log_softmax(x, dim=1)


class MnistDataset(torch.utils.data.Dataset):
    def __init__(self, data_dir):
        trsfm = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.1307,), (0.3081,))
        ])
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)
        self.dataset = datasets.MNIST(
            self.data_dir, train=True, download=True, transform=trsfm)

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx):
        return self.dataset[idx]


class MnistPreProcessor:
    def __init__(self):
        self.trsfm = transforms.Compose([
            transforms.Grayscale(),
            transforms.Resize((28, 28)),
            transforms.ToTensor(),
            transforms.Normalize((0.1307,), (0.3081,))
        ])

    def process(self, x):
        img = PIL.Image.open(x)
        return self.trsfm(img)


class MnistPostProcessor:
    def __init__(self):
        pass

    def process(self, x):
        x = x.argmax(dim=1)
        x = x.detach().cpu().numpy()[0]
        return x.tolist()
