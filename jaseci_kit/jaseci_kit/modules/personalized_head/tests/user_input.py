import torch
from torch.nn import functional as F

# test model module by the user

class LeNet(torch.nn.Module):
    def __ini__(self, num_classes=10):
        super().__init__()
        self.conv1 = torch.nn.Conv2d(1, 6, 5)
        self.pool = torch.nn.MaxPool2d(2, 2)
        self.conv2 = torch.nn.Conv2d(6, 16, 5)
        self.fc1 = torch.nn.Linear(16 * 5 * 5, 120)
        self.fc2 = torch.nn.Linear(120, 84)
        self.fc3 = torch.nn.Linear(84, num_classes)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 16 * 5 * 5)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x


class LeNetDataset(torch.utils.data.Dataset):
    def __init__(self, num_classes=10):
        self.data = torch.randn(100, 1, 28, 28)
        self.labels = torch.randint(0, num_classes, (100,))

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        return self.data[index], self.labels[index]

class LeNetPreProcessor:
    def __init__(self):
        None

    def __call__(self, data):
        return data

class LeNetPostProcessor:
    def __init__(self):
        None

    def __call__(self, data):
        data = torch.argmax(data, dim=1)
        return data
