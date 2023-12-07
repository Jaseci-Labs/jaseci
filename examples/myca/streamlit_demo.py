import streamlit as st

# Display a title and a text block
st.title("Welcome to my Streamlit app!")
st.write("This is a very simple app that demonstrates the basics of Streamlit.")

# Display a button and handle its click
if st.button("Click me!"):
    st.write("You clicked the button!")
