---
sidebar_position: 4
title: Creating an Example App using your own LLM model
description: How to create an example app using your own LLM model
---

# Creating an Example App using your own LLM model

First we need to have an application idea. For this tutorial, we will create a simple grammar checker app. The app will take a sentence as input and will return the sentence with the grammar corrected. For example, if the input is `He reads books`, the output will be `He is reading books.`

## Lets create the necessary JAC Walkers

We will need only one walker for this app. The walker will take a sentence as input and will return the sentence with the grammar corrected. We will use the`llm.generate_prompt` action to generate the prompt in correct format and `llm.generate` action to generate the text. The walker will look like this:

```jac
// main.jac
walker correct_grammar {
    has input;
    can llm.generate, llm.generate_prompt;

    prompt = llm.generate_prompt({"instruction": "Correct grammar of the following sentence", "input": input, output: ""});
    report llm.generate(prompt=prompt);
}
```

## Run the Sentinels

Build the JAC Program and Register the Sentinels. and test the walker.

```bash
jaseci> jac build main.jac
jaseci> sentinels register main.jir -set_active true -mode ir
jaseci> walkers run correct_grammar -ctx '{"input": "He reads books"}'
```

## Create a Small Web App

We will use streamlit to create a small web app. Create a file `app.py` and add the following code:

```python
# app.py
import streamlit as st
import requests

SERV_URL = "http://localhost:5001/js/walker_run"
HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': f"token {os.environ('JASECI_TOKEN')}"
}


st.title("Grammar Checker")

sentence = st.text_area("Enter a sentence")

if st.button("Check Grammar"):
    if sentence:
        response = correct_grammar(sentence)
        if response:
            st.info(response)
        else:
            st.write("Something went wrong")
    else:
        st.error("Please enter a sentence")

def correct_grammar(text:str) -> str:
    payload = {
        "name": "correct_grammar",
        "ctx": {
            "input": text
        }
    }
    response = requests.post(SERV_URL, headers=HEADERS, json=payload)
    return response.json()[0]["generated_text"]
```

## Run the App

Use JSCTL to get the JASECI_TOKEN and run the app.

```bash
jaseci> login <jaseci-server-url> # Input the Email and Password
# Copy the Returned Token
```

In another terminal, export the token and run the app.

```bash
export JASECI_TOKEN=<copied-token>
streamlit run app.py
```

Viola! You have created your own app using your own LLM model. You can use this app to check the grammar of any sentence.