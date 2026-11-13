import streamlit as st
from mcp_client import ask_kubernetes
import asyncio
import base64



def set_local_background(image_path):
  with open(image_path, "rb") as f:
    data = f.read()
  encoded = base64.b64encode(data).decode()
  css = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
    """
  st.markdown(css, unsafe_allow_html=True)


set_local_background("background.png")
st.set_page_config(page_title="Kubernetes AI Assistant",  page_icon="☸️")
st.title("☸️ Kubernetes AI Assistant")
st.caption("Ask questions about your Kubernetes cluster")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask something about your cluster...")

if prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing your Kubernetes cluster..."):
            answer = asyncio.run(ask_kubernetes(prompt))

        st.markdown(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
    })