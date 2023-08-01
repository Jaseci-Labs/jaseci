import streamlit as st
import pandas as pd

st.header("LLM Dataset Builder")

# stop re-running
if "dataset" not in st.session_state:
    st.session_state["dataset"] = pd.DataFrame(
        columns=["instruction", "input", "output"]
    )

instruction = st.text_area("Instruction")
_input = st.text_area("Input")
output = st.text_area("Output")

if st.button("Add"):
    if instruction and output:
        st.session_state["dataset"] = pd.concat(
            [
                st.session_state["dataset"],
                pd.DataFrame(
                    [[instruction, _input, output]],
                    columns=["instruction", "input", "output"],
                ),
            ],
            ignore_index=True,
        )
    else:
        st.error("Instruction and output are required")

st.dataframe(st.session_state["dataset"], use_container_width=True)

if st.button("Save"):
    st.session_state["dataset"].to_json("dataset.json", orient="records")
