# AI Voice Assistant Chatbot

A browser-based voice-enabled chatbot built with **Python Flask**,
**Ollama**, and **Llama 3.2**. Users can type or speak questions,
receive LLM-generated responses, and hear the assistant read responses
aloud.

## Features

-   **LLM-powered answers:** Uses the locally running Llama 3.2 model
    through Ollama.
-   **Text chat:** Send questions through the chat input.
-   **Voice input:** Uses the browser's Web Speech API to convert speech
    into text.
-   **Voice output:** Uses the browser's SpeechSynthesis API to read AI
    responses aloud.
-   **Conversation context:** Sends recent conversation messages to the
    backend so the model can respond with context.
-   **Local inference:** Prompts are sent to the local Ollama service
    rather than a hosted LLM API.

## Technology Stack

  Layer                   Technology
  ----------------------- -----------------------
  Backend                 Python, Flask
  Language model          Llama 3.2
  Local model runtime     Ollama
  Frontend                HTML, CSS, JavaScript
  Speech-to-text          Web Speech API
  Text-to-speech          SpeechSynthesis API
  Backend communication   HTTP JSON API

## Project Structure

``` text
AI-Voice-Assistant/
│
├── app.py
├── templates/
│   └── index.html
└── static/
    └── style.css       # Optional, if styles are moved out of index.html
```

## Prerequisites

Install the following:

1.  Python 3.10 or later.
2.  Ollama for Windows, macOS, or Linux: https://ollama.com/download
3.  A modern browser such as Google Chrome or Microsoft Edge.
4.  Sufficient memory and disk space to run the selected language model.

## Installation and Setup

### 1. Clone or download the project

Open a terminal in the project directory.

### 2. Create and activate a virtual environment (recommended)

**Windows CMD:**

``` cmd
python -m venv venv
venv\Scripts\activate
```

**Windows PowerShell:**

``` powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Python dependencies

``` bash
pip install flask requests
```

### 4. Install and download the LLM

Install Ollama from https://ollama.com/download, then run:

``` bash
ollama pull llama3.2
```

Check that the model is available:

``` bash
ollama list
```

The model name in `app.py` should match an installed model tag. The
example configuration uses:

``` python
MODEL = "llama3.2"
```

### 5. Start Ollama

Ollama normally runs as a background application on Windows and macOS.
If it is not already running, start the Ollama application or run:

``` bash
ollama serve
```

The default local API address is:

``` text
http://localhost:11434
```

Test the model before starting Flask:

``` bash
ollama run llama3.2
```

Enter a question and confirm that the model responds.

### 6. Start the Flask application

From the project root:

``` bash
python app.py
```

Open the application in your browser:

``` text
http://127.0.0.1:5000
```

Allow microphone access when the browser asks for permission.

## How It Works

1.  The user types a message or speaks into the microphone.
2.  For voice input, the browser's Speech Recognition API converts
    speech into text.
3.  JavaScript sends the message and recent conversation history to
    Flask using `POST /chat`.
4.  Flask sends the conversation to Ollama's `/api/chat` endpoint.
5.  Llama 3.2 generates a response.
6.  Flask returns the response as JSON.
7.  The browser displays the response and reads it aloud using
    SpeechSynthesis.

## API Reference

### `GET /`

Returns the chatbot interface rendered from `templates/index.html`.

### `POST /chat`

Accepts JSON:

``` json
{
  "message": "Explain artificial intelligence",
  "history": [
    {
      "role": "user",
      "content": "Hello"
    },
    {
      "role": "assistant",
      "content": "Hello! How can I help?"
    }
  ]
}
```

Example response:

``` json
{
  "reply": "Artificial intelligence is..."
}
```

The backend uses the system prompt, recent conversation history, and
current message to create the Ollama chat request.

## Voice Browser Compatibility

-   Speech recognition support varies by browser and operating system.
    Chrome and Edge generally provide the best support for the Web
    Speech API.
-   Microphone permission is required.
-   Browser speech recognition may use a browser/vendor service; it is
    not necessarily processed locally.
-   Speech synthesis uses voices available on the user's device/browser.
-   For deployment outside localhost, use HTTPS to enable microphone
    access reliably.
-   If speech recognition is unavailable, users can still use text chat.

## Troubleshooting

### Ollama returns HTTP 500

First test the model directly:

``` bash
ollama run llama3.2
```

If this fails, the problem is with Ollama or its model runtime, not
Flask. Read the complete Ollama error and repair or reinstall Ollama
using the official installer:

https://ollama.com/download

On Windows, preserve the model directory (usually
`%USERPROFILE%\.ollama`) when reinstalling if you want to avoid
downloading models again. Do not delete it unless you intentionally want
to remove downloaded models.

### Connection refused at `localhost:11434`

Make sure Ollama is running:

``` bash
ollama serve
```

If Ollama is already running as a background application, do not start a
second server process.

### Model not found

Check installed models:

``` bash
ollama list
```

Download the model if needed:

``` bash
ollama pull llama3.2
```

Make sure `MODEL` in `app.py` matches the installed model name.

### Microphone is not working

-   Allow microphone permission in browser settings.
-   Use Chrome or Edge.
-   Check that the microphone is connected and selected as the system
    input device.
-   Use `localhost` during local development or HTTPS for a deployed
    site.

### Flask cannot import a package

Activate the virtual environment and install dependencies:

``` bash
pip install flask requests
```

## Configuration

The example backend uses these settings in `app.py`:

``` python
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.2"
```

Change `MODEL` only to a model that is installed in Ollama. The system
prompt can also be edited to change the assistant's name, personality,
and response style.

## Limitations and Security Notes

-   This is a local development project, not a production-hardened
    service.
-   The model's speed and response quality depend on available hardware
    and model size.
-   The current browser speech recognition implementation depends on
    browser support and may rely on an external speech service.
-   Do not expose Flask's development server or Ollama's local API
    directly to the public internet.
-   Before public deployment, add authentication, input validation, rate
    limiting, secure configuration, and a production WSGI server.
-   `debug=True` should be disabled in production.
-   Conversation history in the provided frontend is held in browser
    memory and is not permanently saved.

## Future Enhancements

-   Persistent conversation history using MongoDB or SQLite.
-   Multilingual speech input and output.
-   Dedicated speech recognition using Whisper.
-   More natural text-to-speech using a dedicated TTS engine.
-   Wake-word detection.
-   Retrieval-Augmented Generation (RAG) for answering questions from
    PDFs and other documents.
-   Optional web search and personal-assistant actions.

## License

Add a license file before distributing this project. If no license is
included, all rights remain with the copyright holder.
