import streamlit as st
from ollama import chat
from ollama import ChatResponse
import time
import requests
import json


if "model" in st.query_params:
    st.session_state.model = st.query_params.model
else:
    st.session_state.model = "deepseek-r1:1.5b"

if "button_disabled" not in st.session_state:
    st.session_state.download_disabled = False


API_URL = "http://localhost:11434/api"

QUESTIONS = [
    "How much is is 1+4?",
    "Why is the sky blue, in 2 sentences?",
    "Tell me about the bombing of Dresden during 2nd World War in 3 sentences.",
    "What happened in 1989 on Tiananmen?",
    "What is your context window size?",
]

_start = time.time()


def load_question(input_question):
    st.session_state.input_question = input_question


def model_exists(model):
    res = requests.get(f"{API_URL}/tags")
    if res:
        res_json = res.json()
        if not "models" in res_json:
            return False
        for maybe_model in res_json["models"]:
            if maybe_model["name"] == model:
                return True
    # st.write(res.json())

    return False


def disable_download_button():
    st.session_state.download_disabled = True


st.title("Playing with DeepSeek")

with st.sidebar:
    if not model_exists(st.session_state.model):
        if st.button(
            f"Download model: {st.session_state.model}",
            use_container_width=True,
            disabled=st.session_state.download_disabled,
            on_click=disable_download_button,
        ):
            with st.spinner(f"Downloading {st.session_state.model}"):
                st.write(
                    requests.post(
                        f"{API_URL}/pull", data=json.dumps({"model": st.session_state.model})
                    )
                )
    else:
        st.write(f"Model {st.session_state.model} exists.")

    st.markdown("""### Example questions:""")
    for question in QUESTIONS:
        st.button(
            question,
            type="secondary",
            on_click=load_question,
            kwargs={"input_question": question},
            use_container_width=True,
        )


def do_stream():
    for chunk in stream:
        yield chunk["message"]["content"]


q = st.text_input(
    f"Feel free to ask questions to see how the {st.session_state.model} behaves.",
    key="input_question",
)

if q:
    stream = chat(
        model=st.session_state.model,
        messages=[{"role": "user", "content": q}],
        stream=True,
    )
    st.write_stream(do_stream)
    st.write(f"Duration: {round(time.time()-_start, 4)}s")
