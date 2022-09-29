# Personalized Head

**What is Personalized Head:**
Using the Personalized Head module, you can create a custom model head which you can train over the time.
You can use your own custom models and datasets to create a personalized head with just using a configuration
file and a python file.

## **1. Using the Personalized Head as a Standalone Module**
You can use the personalized head as a full custom model other than being a head of a model. For an example you can
for a YOLO model, that you can train and inference. Follow the steps below to use the personalized head as a standalone model. Example shows how to use the personalized head as a MNIST Classification model.

### **1.1. Creating Custom Python Model**
Python File contains the torch.nn.Module class which is the model. You can use any model you want. and a torch.utils.data.Dataset class which is the dataset. You can use any dataset you want. and Preprocessor and Postprocessor classes which are used in inferencing. You can use any preprocessor and postprocessor you want but with the same method format. follow it to create your custom python model.

```python
# Path: ./user_input.py
import torch
from torch.nn import functional as F
from torchvision import datasets, transforms
import os
import PIL

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
```

### **1.2. Creating a Configuration File**
Configuration file is YAML file which contains the information about the model and training parameters. You can follow this example yaml file as a reference to create your own configuration file.

```yaml
#Path: ./config.yaml
# Inference Configuration
Inference:
  postprocess:
    type: CustomProcessor
    args:
      python_file: user_input.py
      module_name: MnistPostProcessor
  preprocess:
    type: CustomProcessor
    args:
      python_file: user_input.py
      module_name: MnistPreProcessor
  weights: ""

# Custom Model Configuration
Model:
  args:
    python_file: user_input.py
    module_name: MnistModel
    num_classes: 10
  type: CustomModel

# Training Configuration (Optional: If you want to train the model)
Trainer:
  name: MnistTrainer
  dataloader:
    args:
      python_file: user_input.py
      module_name: MnistDataset
      batch_size: 32
      data_dir: data/
      num_workers: 1
      shuffle: true
      validation_split: 0.2
    type: CustomDataLoader
  loss: nll_loss
  lr_scheduler:
    args:
      gamma: 0.1
      step_size: 50
    type: StepLR
  metrics:
    - accuracy
    - top_k_acc
  n_gpu: 1
  optimizer:
    args:
      amsgrad: true
      lr: 0.001
      weight_decay: 0
    type: Adam
  trainer:
    early_stop: 10
    epochs: 100
    monitor: min val_loss
    save_dir: saved/
    save_period: 1
    tensorboard: true
    verbosity: 2
```
### **1.3. Create your JAC program**
```python
# Path: ./main.jac
walker identify_number {
  has input_image;
  can personalized_head.create_head, personalized_head.predict;

  root {
      uid = personalized_head.create_head(config_file='config.yaml', uuid='mnist');
      pred = personalized_head.predict(uuid=uid, data=input_image);
      report pred;
  }
}

walker init {
  has input_image;
  has output;

  root {
      spawn here identify_number(input_image=input_image);
  }
}

```

### **1.4. Import 'personalized_head' module in jaseci**
- Open the terminal and run Jaseci Command Line Tool using the command below.
```bash
jsctl -m
```
- Load the 'personalized_head' module using the command below.
```bash
actions load module jaseci_kit.personalized_head
```
- Run the JAC program using the command below.
```bash
jac run main.jac
```

## **2. Using the Personalized Head with another Module**
Coming Soon...
