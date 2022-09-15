# Build a Custom Jaseci Module

In this tutorial, you are going to learn how to build a custom jaseci module with python. In this application I will teach you how to create a basic calculator module for jaseci.

Excited? Hell yeah! Let's jump in.

## Preparation
Let's start by creating a folder called `calculator` in your root directory of your application. After creating the folder let's create a file name `calculator.py` inside of the `calculator` folder.

> **Note**
>
> we are using python to create the custom jaseci module so you will need .py files and not jac.

After creating the file, open the file in a code editor and let's start coding our module.

```py
from jaseci.actions.live_actions import jaseci_action
```
First, we will have to import jaseci_actions to the `calculator.py` file. We will be using jaseci actions to load the module into jaseci.

```py
@jaseci_action(act_group=["timestamp"], allow_remote=True)
```
In this block:
- `act_group` is the name of the jaseci action group called when loading a the module.
- `allow_remote` indicates whether you want this action to be run remotely or not.


We will be adding onto the file.
```py
@jaseci_action(act_group=["timestamp"], allow_remote=True)
def add(first_number: int, second_number: int):
    return first_number + second_number
```

What this functions does, it adds the two numbers from the parameter and returns the sum of each number.

> **Note**
>
> Practice adding data type to the parameters for e.g. `first_number: int` because jaseci_actions use this as validation, remotely and also through the jaseci application.  

## Loading the custom module (API)
In this section, I will run you through how to load the custom module through the API.
```bash
> uvicorn calculator:serv_actions 
```

We use uvicorn to run modules remotely.

> **Note**
>
> `calculator` is folder name and the path in which the module is located and `serv_actions` will allow you to run all functions remotely at one time.


```
←[33mWARNING←[0m:  ASGI app factory detected. Using it, but please consider setting the --factory flag explicitly.
←[32mINFO←[0m:     Started server process [←[36m15604←[0m]
←[32mINFO←[0m:     Waiting for application startup.
←[32mINFO←[0m:     Application startup complete.
←[32mINFO←[0m:     Uvicorn running on ←[1mhttp://127.0.0.1:8000←[0m (Press CTRL+C to quit)
```

You will see something like this and if it shows this you are ready to test out the jaseci custom module.

Go to http://localhost:8000/docs and you can test out your module to see if it works remotely.

# Loading the custom module (JAC)
In this section, I will run you through how to load the custom module through the Jac application.

```bash
> actions load local calculator/calculator.py
```

Since we are creating our own module we have to use the term `local` instead of module or remote. After local is the path to where the module is located.

```
{
  "success": true
}
```
You should see this after running the command. If you see this you have successfully build a custom module using jac with Jaseci.

# How to use the custom module (JAC)
In this section we will show you how to use the custom module in the jac application.

Create a file name main.jac and add the following code.

```js
walker init {
    can calculator.add;
    report calculator.add(1,1);
}
```

This allows you to load the module `can (act_group created)(function created for the act_group);`
``` js
can calculator.add;
```

We will report the result from the calculation.
``` js
report calculator.add(1,1);
```

The following will be the result after running the init walker.
```bash
{
  "success": true,
  "report": [
    2
  ],
  "final_node": "urn:uuid:04e97f70-26b3-467e-a291-bd03b18e7a6d",
  "yielded": false
}
```

Once you see that status it means that everything is working perfectly. Simple right! Hope you learn't something new today.

# Creating A Custom AI Jaseci Module
In this section, we will be creating a t5 based summarization module for jaseci. So let's get started.
### Imports
```py
import torch
from jaseci.actions.live_actions import jaseci_action
from transformers import T5Tokenizer, T5ForConditionalGeneration  # , T5Config
```
In this block:
- We have imported the package `torch`: An open source machine learning framework that accelerates the path from research prototyping to production deployment.
- We also imported `jaseci_action` so we can use it's functionalities to attach it to the jac application.
- Since we are creating a summarization module called t5 it comes with it modules in the form of `transformers`.

### Brining in models
```py
model = T5ForConditionalGeneration.from_pretrained("t5-small")
tokenizer = T5Tokenizer.from_pretrained("t5-small")
device = torch.device("cpu")
```

In this block:
- we will be using the t5-small pretrained model because these models can be very big.

### Generating summary based on text

```py
def t5_generate_sum(text, min_length, max_length):
```
Here, we will be creating a function that generates a summary, we will be intaking parameters such as text (which will be the body of data you want to summarize), min_length (this will be the minimum of words you would like the summarization model to spit out), max_length (which will be the maximum of being returned from the summarization model). So let's get to the next line.

```py
preprocess_text = text.strip().replace("\n", "")
```
This will help us remove new line from any body of text that the user might have inputed to the model. This can mess up the model and return a ugly comprehensive data of the text.

```py
t5_prepared_Text = "summarize: " + preprocess_text
```
The T5 summarization model requires that you append `summarize` infront the body of text used to summarize.

```py
tokenized_text = tokenizer.encode(t5_prepared_Text, return_tensors="pt").to(device)
```
This will encode the text so the AI model can understand and process it.

```py
summary_ids = model.generate(
        tokenized_text,
        num_beams=4,
        no_repeat_ngram_size=2,
        min_length=min_length,
        max_length=max_length,
        early_stopping=True,
    )
```
Using the T5 model this will generate the summary based on the paramater we passed in min_length, max_length, tokenized_text and etc.

```py
output = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
return output
```
Here, based on the result from the encoded summary generated from the AI model we will decode the summarized version of the encoded body of text and return it to the user.

### Function to return summary to Jac or API
```py
@jaseci_action(act_group=["t5_sum"], allow_remote=True)
def classify_text(text: str, min_length: int = 30, max_length: int = 100):
    output = t5_generate_sum(text, min_length, max_length)
    return output
```
In this block:
- Since we created a function which generates the summary. we need a jaseci action function that will bind the summarization module to jac and to the API. 
- here we called the action group `t5_sum`.

### Full Code
```py
import torch
from jaseci.actions.live_actions import jaseci_action
from transformers import T5Tokenizer, T5ForConditionalGeneration  # , T5Config

# from fastapi import HTTPException

model = T5ForConditionalGeneration.from_pretrained("t5-small")
tokenizer = T5Tokenizer.from_pretrained("t5-small")
device = torch.device("cpu")


# generates summary based on text
def t5_generate_sum(text, min_length, max_length):
    preprocess_text = text.strip().replace("\n", "")
    t5_prepared_Text = "summarize: " + preprocess_text

    tokenized_text = tokenizer.encode(t5_prepared_Text, return_tensors="pt").to(device)

    summary_ids = model.generate(
        tokenized_text,
        num_beams=4,
        no_repeat_ngram_size=2,
        min_length=min_length,
        max_length=max_length,
        early_stopping=True,
    )

    output = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    return output


# summarize a large body of text using t5 model (small model)
# which returns data at a fast rate.
@jaseci_action(act_group=["t5_sum"], allow_remote=True)
def classify_text(text: str, min_length: int = 30, max_length: int = 100):
    output = t5_generate_sum(text, min_length, max_length)
    return output
```
Once you completed these steps you can reference the above sections to test and it will work. Good luck! This is how you create a custom AI module using Python in Jaseci.