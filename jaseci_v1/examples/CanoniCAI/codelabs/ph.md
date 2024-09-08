# Enhancing User Experience with Personalized Content using PH

In today's world, users have come to expect personalized experiences across all digital platforms, including natural language processing tasks. Personalized content can help engage users, increase brand loyalty, and ultimately lead to a better user experience. In this tutorial, we will show you how to create personalized content using PH (Personalized Head) with the help of Python and Jac, and how it can be used to enhance user experience.

We will guide you through the steps to set up your environment, create your Jac program, and run it to generate personalized content. By the end of this tutorial, you will have the necessary tools to create personalized content for your users, and improve their overall experience with your digital platform. So let's dive in and get started!

## Table of Contents
1. [Introduction](#1-introduction)
2. [Setting up a PH](#2-setting-up-a-ph)
3. [Creating Jac Progam](#3-creating-jac-progam)
4. [Running the Jac Code](#4-running-the-jac-code)

## 1. Introduction
Personalization has become a buzzword in the world of technology. From e-commerce websites to social media platforms, companies are using personalization to improve the user experience and drive engagement. Personalized content is more likely to be consumed and shared, leading to higher conversion rates and increased customer loyalty.

With the rise of large language models (LLMs), it is becoming increasingly important to have solutions that enhance user experience through personalization. One such solution is PH, or Personalized Head. PH is a relatively small model that can be added to existing LLMs to generate personalized content based on a user's preferences and behavior. PH can be implemented as a single layer transformer or as a small neural network with multiple layers, depending on the specific use case.

In this tutorial, we will show you how to implement PH using Python and Jac programming language. We will walk you through the process of setting up a PH, creating a Jac program, and running the code. By the end of this tutorial, you will have a better understanding of how PH works and how you can use it to enhance personalization in your own applications.

## 2. Setting up a PH
Before we can start implementing PH, we need to set up our environment, we expect you have already installed `python`, `jaseci`. Here are the steps you need to follow:

#### Step 1: Install PH module
PH (Personlized Head) is a module in `jaseci-ai-kit`-`jac_misc` can be used to create personailzed model for user. You can install PH using pip:

> pip install jac_misc[ph]

#### Step 2: Creating a `custom.py`
Now that we have installed the PH module, we can create a `custom.py` file to define our personalized model. Here are the steps you need to follow:
1. Create a new Python file called `custom.py` in your project directory.
2. Import the necessary libraries:
```python
import torch
from jac_misc.ph.utils.base import BaseInference
# replace <base_model> with the desired model to get base model embeddings
from jac_nlp.<base_model> import <base_model>
```
3. Define your `CustomLoss` class</br>
This class extends the `torch.nn.Module` class provided by the pytorch. It overrides the forward method to apply the personalized loss function to the model's logits.
```python
class CustomLoss(torch.nn.Module):
    def __init__(self):
        super(CustomLoss, self).__init__()
        # Define your dataset initialization logic here
    def forward(self, outputs, targets):
        # Define your loss function logic here
        return loss_value
```
4. Define your `CustomDataset` class</br>
This class would contain the logic for manipulating train data to tokenized input as expected by base model
```python
class CustomDataset(torch.utils.data.Dataset):
    def __init__(self, train_args):
        super(CustomDataset, self).__init__()
        # Define your dataset initialization logic here
        self.dataset=train_args["train_file"]

    def __getitem__(self, index):
        # Define your dataset manipulation logic here
        return self.dataset[idx]
```

5. Define your `CustomInference` class</br>
This class extends the `BaseInference` class provided by the `PH` module. It overrides the `predict` method to generate personalized output based on the data.
```python
class CustomInference(BaseInference):
    @torch.no_grad()
    def predict(self, data: Any) -> Any:
        # Define your generation logic here
        return output

```
6. Define your `CustomModel` class</br>
This class extends the CustomModel class provided by the PH module. It takes the base model as an argument and overrides the forward method to apply the personalized head to the model's logits.
```python
class CustomModel(torch.nn.Module):
    def __init__(self, model_args):
        super(CustomModel, self).__init__()
        # define PH
        self.ph_layer = nn.TransformerEncoderLayer(
            d_model=model_args["model_dim"],
            nhead=model_args["attn_head"],
            dim_feedforward=model_args["ff_dim"],
            batch_first=True,
        )
    def forward(self, input_id):
        base_outputs = base_model.encode(input_id)
        logits = outputs.logits
        # Apply personalized head
        personalized_logits =  self.ph_layer(base_outputs)
        return personalized_logits
```
7. Define additional methods as required:</br>
This function would contain the logic for how the samples from CustomDataset should be batched together. You can implement a custom collate function to control how the samples are batched and preprocessed for the model.

```python
def collate_fn(samples):
    # Apply custom preprocessing to each sample
    preprocessed_samples = [custom_preprocess(sample) for sample in samples]

    # Use the default collate function to batch the samples together
    batch = torch.utils.data.dataloader.default_collate(preprocessed_samples)

    # Apply any additional custom postprocessing to the batch
    batch = custom_postprocess(batch)

    return batch
```

## 3. Creating Jac Progam
In the Jac program, we are defining a walker named `run_ph` which has the following capabilities: `ph.create_head_list`, `ph.create_head`, `ph.predict`, `ph.train_head`, and `file.load_str`.

First, we are loading the contents of the custom.py file into a variable python_file using the file.load_str capability of the `run_ph` walker.

Next, we are creating a head_list using the ph.create_head_list capability. A head_list is a dictionary containing information about the different heads we have in our system.

Then, we create a personalized head using the ph.create_head capability, and we assign a UUID to it. In this case, we are using the UUID "example".

After creating the personalized head, we train it using the ph.train_head capability. We pass in a configuration object that specifies the details of the trainer and the data that we want to train on. The trainer we are using is CustomTrainer, and we pass the necessary arguments to its initialization function. Similarly, we create a CustomDataloader and pass its initialization arguments in the train_args dictionary. We also specify a custom loss function and its arguments.

Finally, we use the ph.predict capability to generate predictions from the personalized head we created. We pass in the UUID of the head, the data we want to make predictions on, and any additional arguments that are needed by the CustomInference class.


```jac
walker run_ph {
  has ph_id;
  can ph.create_head_list, ph.create_head, ph.predict, ph.train_head;
  can file.load_str;

  root {
    #loading the python script
    python_file = file.load_str("custom.py");

    #creating a head_list
    ph.create_head_list({
        "Model": {
                "args": {
                    "model_args": {
                        # arguments that is needed for CustomModel initialization
                    }
                },
                "type": "CustomModel",
            },
            "Inference": {
                "type": "CustomInference"
            },
        },
        "python": python_file);

    #creating the head
    uid = ph.create_head(uuid='example');

    # training the head
    ph.train_head("uuid": "example",
                "config": {
                    "Trainer": {
                        "name": "CustomTrainer",
                        "trainer": {# arguments to trainer},
                        "dataloader": {
                            "args": {
                                "train_args": {
                                    # arguments that is needed for CustomDataloader initialization
                                }
                            },
                            "type": "CustomDataLoader",
                        },
                        "loss": "custom_loss",
                        "loss_args": {# arguments CustomLoss init},
                        "metrics": [],
                    }
                });

    #predict
    pred = ph.predict("uuid": "example",
                    "data": {
                        "inf_args": {
                            # arguments that needs to be consumed by predict function
                        },
                        "dataset": [
                            "this is a sample data for evaluation"
                        ],
                    });
    report pred;
  }
}

walker init {
  has ph_id;
  root {
      spawn here walker::identify_number(ph_id=ph_id);
  }
```
Overall, the above Jac program sets up the environment for creating and training a personalized head using the PH module, and provides an example of how to make predictions using the personalized head.

## 4. Running the Jac Code
Now that we have created our Jac program, we can run it to see the output. Here are the steps you need to follow:

#### Step 1: Save the Jac code
Save your Jac code to a file named `run_ph.jac` in your project directory.

#### Step 2: Run the Jac code
To run the Jac code, open a terminal window and navigate to your project directory. Then run the following command:

> jsctl -m jac run_ph.jac



### Congratulations!
You have now implemented PH using Python and Jac. By following the steps outlined in this tutorial, you can easily set up your environment, create your Jac program, and run it to generate personalized content based on user preferences for a variety of natural language processing tasks.
