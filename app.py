import os
import datetime
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

st.set_page_config(page_title="Nova — AI Voice Assistant", page_icon="🎙️", layout="centered")
st.title("🎙️ Nova — AI Voice Assistant")
st.caption("A hackathon-ready starter: chat, voice input, text-to-speech, and simple utility commands.")

api_key = os.getenv("OPENAI_API_KEY", "").strip()
if not api_key:
    st.warning("Add your OpenAI API key to a .env file before using AI replies. Utility commands still work.")
client = OpenAI(api_key=api_key) if api_key else None

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I'm Nova. Ask me something, or try: 'what time is it?' or 'help'."}
    ]

def local_command(text: str):
    q = text.lower().strip()
    now = datetime.datetime.now().astimezone()
    if any(x in q for x in ["what time is it", "current time", "time now"]):
        return f"It's {now.strftime('%I:%M %p')} on {now.strftime('%A, %B %d, %Y')}."
    if q in {"help", "what can you do", "commands"}:
        return ("I can answer questions using the AI model, take voice input, speak replies aloud, "
                "tell the current local time, and handle simple greetings. Try asking me to explain a topic.")
    if q in {"hi", "hello", "hey", "namaste"}:
        return "Hello! What would you like help with?"
    return None

def get_ai_reply(history):
    if client is None:
        return "AI replies are not configured yet. Add OPENAI_API_KEY to your .env file, then restart the app."
    try:
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[
                {"role": "system", "content": (
                    "You are Nova, a friendly voice-first personal assistant. "
                    "Be clear, concise, practical, and honest. Do not claim to control devices "
                    "or perform actions you cannot actually perform."
                )},
                *history
            ],
            temperature=0.5,
        )
        return response.choices[0].message.content or "I couldn't form a reply."
    except Exception as e:
        return f"I couldn't reach the AI service. Check your API key, billing, and internet connection. Details: {e}"

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_text = st.chat_input("Ask Nova anything…")
voice_text = None
try:
    audio = st.audio_input("Or speak to Nova (voice input)")
    if audio is not None:
        with st.spinner("Transcribing your voice…"):
            if client is None:
                st.info("Voice transcription needs an OpenAI API key in .env.")
            else:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=("voice.wav", audio.getvalue(), "audio/wav")
                )
                voice_text = transcript.text
                st.success(f"Heard: {voice_text}")
except Exception:
    pass

prompt = user_text or voice_text
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    command = local_command(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            reply = command or get_ai_reply(st.session_state.messages[-12:])
        st.markdown(reply)
        if client is not None:
            try:
                speech = client.audio.speech.create(
                    model="tts-1",
                    voice="alloy",
                    input=reply[:3500]
                )
                st.audio(speech.content, format="audio/mp3")
            except Exception:
                st.caption("Text-to-speech was unavailable for this reply.")
    st.session_state.messages.append({"role": "assistant", "content": reply})

with st.sidebar:
    st.header("About this demo")
    st.write("Nova is a software-only Alexa-like assistant prototype.")
    st.markdown("- Chat with an AI assistant\n- Voice input (microphone)\n- Spoken responses\n- Local time/help commands")
    st.warning("This is a prototype, not a full Alexa replacement. It does not control smart-home devices.")
    if st.button("Clear conversation"):
        st.session_state.messages = []
        st.rerun()
