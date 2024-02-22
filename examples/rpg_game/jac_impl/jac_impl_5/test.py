# # With pipeline, just specify the task and the model id from the Hub.
# from transformers import pipeline
# pipe = pipeline("text-generation", model="distilgpt2")

# # If you want more control, you will need to define the tokenizer and model.
# from transformers import AutoTokenizer, AutoModelForCausalLM
# tokenizer = AutoTokenizer.from_pretrained("distilgpt2")
# model = AutoModelForCausalLM.from_pretrained("distilgpt2")


from hugchat import hugchat
from hugchat.login import Login