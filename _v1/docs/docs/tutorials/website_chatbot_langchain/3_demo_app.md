---
sidebar_position: 3
title: Connecting API with a simple demo app
description: Connecting API with a simple demo app
---

# Connecting API with a simple demo app
We will be using the following streamlit application (Simple Chat Application made using streamlit to interface with OpenAI CHatGPT) as the starting point for our demo app:

```python
import openai
import streamlit as st

st.title("ChatGPT-like clone")

openai.api_key = st.secrets["OPENAI_API_KEY"]

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
```
This will provide a simple chat interface to interact with the OpenAI ChatGPT model. We will be using this as a starting point to connect our API to the chatbot.

![image](https://docs.streamlit.io/images/knowledge-base/chatgpt-clone.gif)

## Connecting the API to the demo app

We will be using the following code to connect the API to the demo app and add them to the starting point code:

```python
import requests

SERV_URL = "http://localhost:5001/js/walker_run" # URL to your jaseci server
HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': f"token {os.environ('JASECI_TOKEN')}"
}

def query(text:str):
    payload = {
        "name": "ask_jaseci_bot",
        "ctx": {
            "input": text
        }
    }
    response = requests.post(SERV_URL, headers=HEADERS, json=payload)
    return response.json()[0] # returns a dict {"input": str, "output": str}
```

Lets change the code to use the query function instead of the OpenAI ChatGPT model:

```python
# Path: app.py

import streamlit as st
import requests

SERV_URL = "http://localhost:5001/js/walker_run" # URL to your jaseci server
HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': f"token {os.environ('JASECI_TOKEN')}"
}

def query(text:str):
    payload = {
        "name": "ask_jaseci_bot",
        "ctx": {
            "input": text
        }
    }
    response = requests.post(SERV_URL, headers=HEADERS, json=payload)
    return response.json()[0]

st.title("Jaseci Bot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = qeury(prompt)["output"]
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
```

## Running the demo app

To run the demo app, you will need to run the following command in the terminal:

```bash
pip install streamlit
streamlit run app.py
```

Simple as that! You should now be able to interact with your Jaseci bot using the demo app.