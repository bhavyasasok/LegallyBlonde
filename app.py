import os
import pickle
import faiss
import numpy as np
import requests
from flask import Flask, request, jsonify, render_template
from sentence_transformers import SentenceTransformer

app = Flask(__name__)

# -------------------------
# Load FAISS index + documents
# -------------------------
index = faiss.read_index("model/constitution.index")

with open("model/articles.pkl", "rb") as f:
    documents = pickle.load(f)

# -------------------------
# Load embedding model
# -------------------------
embed_model = SentenceTransformer("all-MiniLM-L6-v2", local_files_only=True)

def get_embedding(text):
    return np.array(embed_model.encode(text)).astype("float32")


# -------------------------
# Ollama Call (Safe Version)
# -------------------------
def ask_llama(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )

        response.raise_for_status()
        return response.json().get("response", "")

    except Exception as e:
        return f"AI Error: {str(e)}"


# -------------------------
# Serve Frontend
# -------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -------------------------
# ANALYZE ROUTE
# -------------------------
@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.json
        user_problem = data.get("problem")

        if not user_problem:
            return jsonify({"error": "No problem provided"}), 400

        # Embed query
        query_vector = np.array([get_embedding(user_problem)])

        # FAISS search
        distances, indices = index.search(query_vector, 10)

        candidates = []

        for idx, dist in zip(indices[0], distances[0]):
            law_metadata = documents[idx]


            score = 0
            score += (1 / (dist + 1e-5)) * 50

            if law_metadata.get("emergency"):
                score += 30

            if law_metadata.get("gender_specific"):
                score += 15

            score += law_metadata.get("severity_level", 0) * 2

            candidates.append((score, law_metadata))

        candidates.sort(reverse=True, key=lambda x: x[0])
        matched_laws = [law for score, law in candidates[:5]]

        # Build AI context
        law_text_block = ""
        for law in matched_laws:
            law_text_block += f"""
Law Name: {law.get('law_name')}
Act: {law.get('act')}
Category: {law.get('category')}
Description: {law.get('description')}
"""

        # Ask AI with STRICT structured output
        raw_response = ask_llama(f"""
You are a legal support assistant for women in India.

User Problem:
{user_problem}

Relevant Laws:
{law_text_block}

Respond STRICTLY in this format:

YOU ARE HEARD:
(text)

WHAT THE LAW SAYS:
(text)

YOUR NEXT STEPS:
(text)

HELPLINES:
112
181

DISCLAIMER:
This is informational only.
""")

        # -------------------------
        # Parse Structured Sections
        # -------------------------
        heard = ""
        law_section = ""
        steps = ""
        helplines = "Emergency: 112<br>Women Helpline: 181"
        disclaimer = "This is general information, not legal advice."

        try:
            parts = raw_response.split("WHAT THE LAW SAYS:")
            if len(parts) > 1:
                heard = parts[0].replace("YOU ARE HEARD:", "").strip()
                remaining = parts[1]

                parts2 = remaining.split("YOUR NEXT STEPS:")
                if len(parts2) > 1:
                    law_section = parts2[0].strip()
                    remaining2 = parts2[1]

                    parts3 = remaining2.split("HELPLINES:")
                    if len(parts3) > 1:
                        steps = parts3[0].strip()
        except:
            heard = raw_response

        return jsonify({
            "you_are_heard": heard,
            "what_the_law_says": law_section,
            "your_next_steps": steps,
            "helplines": helplines,
            "disclaimer": disclaimer
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -------------------------
# CHAT ROUTE (Required by frontend)
# -------------------------
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        message = data.get("message")

        if not message:
            return jsonify({"response": "Please ask a question."})

        reply = ask_llama(f"""
You are a legal assistant.

User question:
{message}

Answer clearly and concisely.
""")

        return jsonify({
            "response": reply
        })

    except Exception:
        return jsonify({
            "response": "I'm having trouble responding right now."
        })


# -------------------------
# Run Server
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)
