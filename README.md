# Nova — AI Voice Assistant

A beginner-friendly, software-only Alexa-like assistant prototype built with Python, Streamlit, and the OpenAI API.

## Features
- Chat interface
- Voice input through the browser microphone (transcription)
- Spoken replies (text-to-speech)
- Local time, greetings, and help commands
- Simple, clean interface suitable for a hackathon prototype

## Requirements
- Python 3.10 or newer
- Internet connection
- An OpenAI API key with API access/billing enabled for AI, voice transcription, and speech generation

## Run locally

### Windows
1. Install Python from https://www.python.org/downloads/ (enable **Add Python to PATH**).
2. Extract this ZIP.
3. Open the extracted folder in File Explorer.
4. Click the address bar, type `cmd`, and press Enter.
5. Run:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
notepad .env
```

6. Replace `put_your_api_key_here` with your own API key and save the file.
7. Run:

```bash
streamlit run app.py
```

8. Open the local URL shown in the terminal, usually http://localhost:8501.

### macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your API key
streamlit run app.py
```

## Important
- Never upload your `.env` file or API key to GitHub.
- API usage may incur charges depending on your account and model usage.
- The app asks for microphone permission when using voice input.
- Test every feature before recording your demo.
- Do not claim this prototype is an official Amazon Alexa product or that it controls smart devices.

## Hackathon demo checklist
- [ ] Launch the app successfully
- [ ] Test a normal AI question
- [ ] Test voice input and spoken response
- [ ] Test `what time is it?` and `help`
- [ ] Record a short screen demo with your own narration
- [ ] Add screenshots and a truthful description to the submission
- [ ] Publish source code in a GitHub repository without `.env`
