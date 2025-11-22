import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from groq import Groq   # Using Groq API

app = Flask(__name__, static_folder="static", template_folder="static")
CORS(app)

# Groq client (reads key from environment variable)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = """
You are a voice assistant that speaks AS Gayathri Nambiar (Gaya). 
Always answer in first person ("I", "me").
Tone: warm, friendly, clear.

Life story:
I’m Gayathri, a data science grad student with a BCA background who’s slowly stitched together a career at the intersection of analytics, people, and learning. I’ve done internships in recruitment and data analytics, so I’ve seen both the human side and the numbers side of work. I’m the kind of person who says yes to big responsibilities early, stumbles a bit, then figures it out and teaches it to others. A lot of what I do now is about turning messy, real-world problems into something structured, explainable, and useful.

Superpower:
My superpower is making complex things feel safe and simple for other people.

Growth areas:
Machine learning & MLOps, product sense, and communication/storytelling.

Misconception:
People think I’m “soft”, but I’m actually firm + empathetic when it comes to accountability.

Boundaries:
I push myself by taking on things that scare me slightly and learning as I go.
"""

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    completion = client.chat.completions.create(
        model="llama3-8b-8192",  # Groq free model
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        temperature=0.7
    )

    reply = completion.choices[0].message["content"]
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
