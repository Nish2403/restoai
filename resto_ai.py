import requests
import streamlit as st
from gtts import gTTS
import tempfile

st.set_page_config(page_title="Resto AI", layout="centered")
st.title("Welcome to Resto AI ! ")
st.write("A place for finding the best restaurants")
st.write("Just type anything in the message box ! Bon appetite")
OLLAMA_URL = "http://localhost:11434/api/generate"
model_name="my-custom-model"
if "messages" not in st.session_state:
    st.session_state.messages = []
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


prompt = st.chat_input("Ask something...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    payload = {
            "model": model_name,
            "prompt": prompt,
            "stream": False
    }
    response = requests.post(OLLAMA_URL, json=payload)
    if response.status_code == 200:
        answer = response.json()["response"]
    else:
        answer = "❌ Error connecting to Resto AI"
    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)
        tts = gTTS(text=answer, lang="en")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        audio_file = fp.name
    st.audio(audio_file, format="audio/mp3",autoplay=True)



