# Creating a Custom Jaseci Action using T5
In this section, we will be creating a T5 transformer based summarization module for jaseci.
> **Note**
>
> If this is your first time creating a Jaseci action, we recommend going through [this guide](support/codelabs/custom_jaseci_module_codelab.md) first, which covers the basics of creating and loading a custom Jaseci action.

### Imports
```py
import torch
from jaseci.actions.live_actions import jaseci_action
from transformers import T5Tokenizer, T5ForConditionalGeneration  # , T5Config
```
In this block:
- We have imported the package `torch`: an open source machine learning framework that accelerates the path from research prototyping to production deployment.
- We also imported `jaseci_action` so we can use it's functionalities to attach it to the jac application.
- Since we are creating a summarization module called t5 it comes with it modules in the form of `transformers`.

### Bring in models
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

Once you have completed these steps, load the module using the actions load local command as shown below:

```bash
> actions load local path/to/t5_sum.py
```
Depending on your environment and machine, you might see certain warnings or logging messages, which are expected and normal. If you see `success: true` that means the module is built and loaded correctly.

Here is a simple jac example to use the new T5 summarize action
```js
walker init {
    can t5_sum.classify_text;
    report t5_sum.classify_text("Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.");
}
```