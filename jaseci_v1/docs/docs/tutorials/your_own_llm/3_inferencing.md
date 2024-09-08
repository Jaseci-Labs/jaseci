---
sidebar_position: 3
title: Inferencing your model using JAC Language
description: How to use your own Instruction model to generate texts using JAC Language
---

# Inferencing your model

There are couple of ways to interface with your own llm model. But first you need to load the trained model. You can load the model using the following command:

```bash
jaseci> actions call llm.setup -ctx '{"model_name": "databricks/dolly-v2-3b", "lora_dir": "<your_output_dir>/final"'
```
This will load the pretrained model and lora you have just trained. You can check whether the model is loaded or not using the following command:

```bash
jaseci> actions call llm.generate -ctx '{"prompt": "Hello, how are you?"}'
```

## Using JAC Language

Once you have loaded the model, you can use the `generate` action to generate text. The `generate` action allows you to generate text based on the input text you provide.

```jac
# main.jac
walker generate_text {
    has instruction = "Convert the following sentence into the present continuous tense";
    has input;

    can llm.generate, llm.generate_prompt;

    prompt = llm.generate_prompt({"instruction": instruction, "input": input, output: ""});
    report llm.generate(prompt="Hello, how are you?");
}
```

Build the JAC Program and Register the Sentinels

```bash
jaseci> jac build main.jac
jaseci> sentinels register main.jir -set_active true -mode ir
```

Run the walker
```bash
jaseci> walkers run generate_text -ctx '{"input": "He reads books"}'
```

Output
```json
[
    {
        "generated_text": "He is reading books."
    }
]
```

If running on a server, you can use the following python to run the walker:

```python
import requests

url = "http://localhost:8000/js/walker_run"
payload = {
    "name": "llm.generate",
    "ctx": {
        "prompt": "Hello, how are you?"
    }
}
headers = {
    "Content-Type": "application/json",
    "Authorization": f"token {os.getenv('JASECI_TOKEN')}",
}

response = requests.request("POST", url, json=payload, headers=headers)
print(response.json())
```


## Using the Action Directly (Only Works with Jaseci Server and with Admin Access)

Assuming you have llms module running in the server and you have loaded the model using the `setup` action, you can use the `generate` action to generate text. The `generate` action allows you to generate text based on the input text you provide.

```python
import requests

url = "http://localhost:8000/js_admin/actions_call"
payload = {
    "name": "llm.generate",
    "ctx": {
        "prompt": "Hello, how are you?"
    }
}
headers = {
    "Content-Type": "application/json",
    "Authorization": f"token {os.getenv('JASECI_TOKEN')}",
}

response = requests.request("POST", url, json=payload, headers=headers)
print(response.json())
```