
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.2"

SYSTEM_PROMPT = """
You are a friendly and intelligent AI voice assistant.

Your name is Hari's AI Assistant.

Answer questions clearly and naturally.
Keep answers conversational and easy to understand.
You can answer questions about programming, AI,
technology, education, science and general knowledge.
If you don't know something, be honest.
"""

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():

    try:
        data = request.json

        user_message = data.get("message", "")
        history = data.get("history", [])

        if not user_message.strip():
            return jsonify({"reply": "Please enter a message."}), 400

        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]

        # Maintain previous conversation
        for item in history[-10:]:
            if item.get("role") in ["user", "assistant"]:
                messages.append({
                    "role": item["role"],
                    "content": item["content"]
                })

        messages.append({
            "role": "user",
            "content": user_message
        })

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "messages": messages,
                "stream": False
            },
            timeout=120
        )

        response.raise_for_status()

        result = response.json()

        ai_reply = result["message"]["content"]

        return jsonify({
            "reply": ai_reply
        })

    except requests.exceptions.ConnectionError:
        return jsonify({
            "reply": "Ollama is not running. Please start Ollama."
        }), 503

    except requests.exceptions.Timeout:
        return jsonify({
            "reply": "The AI is taking too long to respond. Try again."
        }), 504

    except Exception as e:
        return jsonify({
            "reply": f"Something went wrong: {str(e)}"
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
