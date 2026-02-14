import os
import json
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request, jsonify, render_template
from sentence_transformers import SentenceTransformer
from groq import Groq
from pinecone import Pinecone

app = Flask(__name__)

# -------------------------
# Initialize Groq Client
# -------------------------
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# -------------------------
# Initialize Pinecone
# -------------------------
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
pinecone_index = pc.Index("women-legal-rag")

# -------------------------
# Load Embedding Model
# -------------------------
embed_model = SentenceTransformer("all-MiniLM-L6-v2")


# -------------------------
# Serve Frontend
# -------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -------------------------
# ANALYZE ROUTE (RAG + Groq)
# -------------------------
@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.json
        user_problem = data.get("problem")

        if not user_problem:
            return jsonify({"error": "No problem provided"}), 400

        # 1️⃣ Embed user query
        query_embedding = embed_model.encode(user_problem).tolist()

        # 2️⃣ Query Pinecone
        results = pinecone_index.query(
            vector=query_embedding,
            top_k=5,
            include_metadata=True
        )

        matches = results.matches if hasattr(results, "matches") else results.get("matches", [])

        if not matches:
            return jsonify({
                "related_laws": [],
                "you_are_heard": "We understand this is a difficult situation.",
                "what_the_law_says": "No relevant laws were found in the database.",
                "your_next_steps": "Please consult a legal professional.",
                "helplines": "112, 181",
                "disclaimer": "This is informational only."
            })

        # 3️⃣ Extract Related Laws + Build Context
        law_text_block = ""
        related_laws = []

        for match in matches:
            metadata = match.metadata if hasattr(match, "metadata") else match.get("metadata", {})

            law_data = {
                "law_id": metadata.get("law_id", "N/A"),
                "law_name": metadata.get("law_name", "N/A"),
                "act": metadata.get("act", "N/A"),
                "category": metadata.get("category", "N/A"),
                "description": metadata.get("description", "N/A"),
                "emergency": metadata.get("emergency", False),
                "severity_level": metadata.get("severity_level", 0),
                "gender_specific": metadata.get("gender_specific", False)
            }

            related_laws.append(law_data)

            law_text_block += f"""
        Law ID: {law_data['law_id']}
        Law Name: {law_data['law_name']}
        Act: {law_data['act']}
        Category: {law_data['category']}
        Description: {law_data['description']}
        """


        # 4️⃣ Call Groq LLM
        chat_completion = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            temperature=0.2,
            max_tokens=800,
            messages=[
                {
                    "role": "system",
                    "content": """You are a legal support assistant for women in India.

You MUST:
- Use ONLY the retrieved laws provided.
- Do NOT fabricate laws.
- Be supportive but legally grounded.
- Respond ONLY in valid JSON.
"""
                },
                {
                    "role": "user",
                    "content": f"""
User Problem:
{user_problem}

Retrieved Laws:
{law_text_block}

Respond ONLY in this JSON format:

{{
  "you_are_heard": "...",
  "what_the_law_says": "...",
  "your_next_steps": "...",
  "helplines": "112, 181",
  "disclaimer": "This is informational only."
}}

Return JSON only.
"""
                }
            ]
        )

        raw_response = chat_completion.choices[0].message.content.strip()

        # 5️⃣ Parse JSON safely
        try:
            parsed = json.loads(raw_response)

            return jsonify({
                "related_laws": related_laws,   # ✅ Now returned
                "you_are_heard": parsed.get("you_are_heard", ""),
                "what_the_law_says": parsed.get("what_the_law_says", ""),
                "your_next_steps": parsed.get("your_next_steps", ""),
                "helplines": parsed.get("helplines", "112, 181"),
                "disclaimer": parsed.get("disclaimer", "This is informational only.")
            })

        except Exception:
            # If LLM fails to return JSON
            return jsonify({
                "related_laws": related_laws,
                "you_are_heard": "We understand this is a difficult situation.",
                "what_the_law_says": raw_response,
                "your_next_steps": "Please consult a legal professional.",
                "helplines": "112, 181",
                "disclaimer": "This is informational only."
            })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -------------------------
# CHAT ROUTE
# -------------------------
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        message = data.get("message")

        if not message:
            return jsonify({"response": "Please ask a question."})

        chat_completion = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            temperature=0.4,
            max_tokens=500,
            messages=[
                {"role": "system", "content": "You are a helpful legal assistant."},
                {"role": "user", "content": message}
            ]
        )

        reply = chat_completion.choices[0].message.content

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
    app.run(host="0.0.0.0", port=5001, debug=True)
