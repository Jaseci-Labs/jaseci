import:py streamlit as st;


can sl_start {
    import:py subprocess;
    import:py sys;
    if ".jac" in " ".join(sys.argv) {subprocess.run(["streamlit", "run", "__jac_gen__/streamlit_demo.py"]);}
}


with entry {
    # Display a title and a text block
    sl_start();
    st.title("Welcome to my Streamlit app!");
    st.write("This is a very simple app that demonstrates the basics of Streamlit.");

    # Display a button and handle its click
    if st.button("Click me!"){st.write("You clicked the button!");}
}