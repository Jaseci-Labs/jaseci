import streamlit as st
from streamlit_chat import message
import requests
import os
from dotenv import load_dotenv

load_dotenv()

SERV_URL = "http://localhost:5001/js/walker_run"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"token {os.getenv('JASECI_TOKEN')}",
}

EXAMPLE_CONTEXT = """
Mount Lavinia (Sinhala: ගල්කිස්ස, Tamil: கல்கிசை) is a suburb in Colombo, Sri Lanka located within the administrative boundaries of the Dehiwala-Mount Lavinia municipal limits.
The area is a mostly residential suburb, known as Colombo's beach retreat it is famed for its "Golden Mile" of beaches[1][2] and has long been a hot spot for tourism and nightlife. It is one of the most liberal regions in Sri Lanka and plays host to the island's annual Gay Pride and Rainbow Kite Festival since 2005.[3][4]
The area's name arose when the second Governor of Ceylon, Sir Thomas Maitland, acquired land at "Galkissa" (Mount Lavinia) and decided in 1806 to construct a personal residence there. Maitland fell in love with Lovina Aponsuwa, a local mestiço dancer, and continued a romantic affair with her until he was recalled to England in 1811. The Governor's mansion, which he named "Mount Lavinia House" is now the Mount Lavinia Hotel and the village that surrounded the building has subsequently developed into a bustling area, taking its name from the Governor's mistress, Lovina.
There are other explanations rooted in geography and the natural surroundings, when it comes to the origin of the name Mount Lavinia. The Sinhalese who lived on the coastal belt had named the promontory "Lihiniya Kanda" (Sinhala: ලිහිණියා කන්ද) or "Lihiniyagala" (Sinhala: ලිහිණියාගල) meaning the hill of the sea gull or the rock of the sea gull.
The local name for the town today is Galkissa - Kissa being a somewhat obsolete Sinhala word for rock.
The town came into official recognition when Governor Maitland used the postal address Mt. Lavinia, Ceylon, in 1805, while writing to the British Secretary of State, Lord Castlereagh.
The suburb also boasts S.Thomas' College, one of Sri Lanka's most prestigious primary and secondary schools.
"""

st.title(":rocket: Document Retrieval Conversational Chatbot")
st.markdown(
    "This is a demo of using Jaseci's langchain module to build a conversational chatbot that can have a conversation with you for a given text."
)

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []


def get_text():
    input_text = st.text_input("You: ", "Hello, how are you?", key="input")
    return input_text


def query(question, chat_history):
    payload = {
        "name": "query",
        "ctx": {"question": question, "chat_history": chat_history},
    }
    response = requests.post(SERV_URL, headers=HEADERS, json=payload)
    return response.json()["report"][0]


def setup_langchain(context, openai_api_key):
    payload = {
        "name": "update_chain",
        "ctx": {"text": context, "openai_api_key": openai_api_key},
    }
    response = requests.post(SERV_URL, headers=HEADERS, json=payload)
    return response.json()["success"]


st.markdown("## Set Context")
st.markdown(
    "Enter the text you want to use as context for the chatbot. This can be a text file or a text string."
)

context = st.text_area("Context: ", EXAMPLE_CONTEXT, key="context")
openai_key = st.text_input("OpenAI Key: ", key="openai_key")
if st.button("Set Context", key="set_context") and context:
    if not openai_key:
        openai_key = os.getenv("OPENAI_API_KEY")
        if not openai_key:
            st.error(
                "OpenAI API key not found. Please enter your key or set the OPENAI_API_KEY environment variable."
            )
            st.stop()
    with st.spinner("Setting up context..."):
        setup_langchain(context, openai_key)


st.markdown("## Chatbot")
user_input = get_text()
if st.button("Submit", key="submit") and user_input:
    with st.spinner("Thinking..."):
        output = query(user_input, st.session_state["chat_history"])
        st.session_state["chat_history"].append((user_input, output["answer"]))

if st.session_state["chat_history"]:
    for i in range(len(st.session_state["chat_history"]) - 1, -1, -1):
        message(st.session_state["chat_history"][i][0], key=str(i))
        message(
            st.session_state["chat_history"][i][1], is_user=True, key=str(i) + "_user"
        )
