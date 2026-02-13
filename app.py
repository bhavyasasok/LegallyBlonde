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
    documents = pickle.load(f)  # contains FullText + metadata

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
                "model": "mistral",   # or phi3 if installed
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )

        response.raise_for_status()
        return response.json().get("response", "No response from model.")

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

        # Embed user query
        query_vector = np.array([get_embedding(user_problem)])

        # Search FAISS (top 10 for better ranking)
        distances, indices = index.search(query_vector, 10)

        candidates = []

        for idx, dist in zip(indices[0], distances[0]):
            law_metadata = documents[idx]["metadata"]

            score = 0

            # Similarity boost (lower distance = better match)
            score += (1 / (dist + 1e-5)) * 50

            # Emergency laws boost
            if law_metadata.get("emergency"):
                score += 30

            # Gender-specific boost
            if law_metadata.get("gender_specific"):
                score += 15

            # Severity level boost
            score += law_metadata.get("severity_level", 0) * 2

            candidates.append((score, law_metadata))

        # Sort by best score
        candidates.sort(reverse=True, key=lambda x: x[0])

        # Select top 5
        matched_laws = [law for score, law in candidates[:5]]

        # Build law text block for AI
        law_text_block = ""

        for law in matched_laws:
            law_text_block += f"""
Law Name: {law.get('law_name')}
Act: {law.get('act')}
Category: {law.get('category')}
Description: {law.get('description')}

"""

        # Ask Local AI
        analysis = ask_llama(f"""
You are a legal support assistant for women in India.

User Problem:
{user_problem}

Relevant Laws:
{law_text_block}

Tasks:
1. Summarize the issue.
2. Explain applicable legal protections.
3. Suggest practical next steps.
4. Include helplines:
   - 112
   - 181
5. Add disclaimer: Informational only.

Be supportive.
Do not fabricate laws.
""")

        return jsonify({
            "query": user_problem,
            "matched_laws": matched_laws,
            "analysis": analysis,
            "helplines": "112 (Emergency), 181 (Women Helpline India)",
            "disclaimer": "This is informational only and not a substitute for a lawyer."
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -------------------------
# Run Server
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)
