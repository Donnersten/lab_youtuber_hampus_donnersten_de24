import streamlit as st
import requests
from pathlib import Path

ASSETS_PATH = Path(__file__).absolute().parents[1] / "assets"

def layout():

    st.markdown("# Youtube Bot")
    st.markdown("Ask a question about different the youtube videos")
    text_input = st.text_input(label="Ask a questions")

    if st.button("Ask") and text_input.strip() != "":
        response = requests.post(
            "http://127.0.0.1:8000/rag/query", json={"prompt": text_input}
        )

        data = response.json()
        cols = st.columns(2)

        with cols[0]:
            st.markdown("## Question:")
            st.markdown(text_input)
            with st.expander("## Source:"):
                st.markdown(data["filepath"])

        with cols[1]:
            st.markdown("## Answer:")
            st.markdown(data["answer"])


if __name__ == "__main__":
    layout()