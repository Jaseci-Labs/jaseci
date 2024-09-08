# Document Retrieval Conversational Chatbot using Jaseci's Langchain
This is a demo of using Jaseci's langchain module to build a conversational chatbot that can have a conversation with you for a given text.

## How to use
Install necessary packages
```bash
pip install -r requirements.txt
```
Create jaseci-server instance
```bash
jsserv runserver 5001
```
Run JSCTL and run the following commands
```bash
jsctl -m
jaseci> jac build main.jac
jaseci> login http://localhost:5001 # Input email and password, keep the token
jaseci> actions load module jac_misc.langchain
jaseci> sentinel register main.jir -set_active true -mode ir
```
Update the `.env` file with the token and openai api key
```env
JASECI_TOKEN=YOUR_TOKEN
OPENAI_API_KEY=YOUR_KEY
```
Run the streamlit frontend
```bash
streamlit run app.py
```

## Preview

<a href="https://imgbb.com/"><img src="https://i.ibb.co/hyR1sXv/Screen-Recording-2023-06-01-at-21-24-18.gif" alt="Screen-Recording-2023-06-01-at-21-24-18" border="0"></a>