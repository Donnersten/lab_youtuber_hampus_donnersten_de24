import streamlit as st
import requests
from pathlib import Path
import os 
from dotenv import load_dotenv

load_dotenv()

ASSETS_PATH = Path(__file__).absolute().parents[1] / "assets"
url = f"https://labb-youtuber.azurewebsites.net/rag/query?code={os.getenv('FUNCTION_APP_API')}"


def layout():
    st.title("Youtube Bot")
    st.caption("Ask a question about different the youtube videos")
    st.session_state.setdefault(
        "messages", [{"role": "assistant", "content": "How can I help you?"}]
    )

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    prompt = st.chat_input("Ask a question")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        response = requests.post(url, json={"prompt": prompt})
        response.raise_for_status()
        data = response.json()
        answer = data.get("answer")
        source = data.get("filepath")

        st.session_state.messages.append({"role": "assistant", "content": answer})
        with st.chat_message("assistant"):
            st.write(answer)
            if source:
                st.caption(f"Source: {source}")


if __name__ == "__main__":
    layout()
