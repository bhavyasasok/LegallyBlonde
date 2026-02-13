import os
import json
from dotenv import load_dotenv
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer

load_dotenv()

# Initialize Pinecone
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("women-legal-rag")

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load your law data
with open("data/women_laws.json", "r", encoding="utf-8") as f:
    laws = json.load(f)

print("Total laws:", len(laws))

vectors = []

for i, law in enumerate(laws):
    full_text = f"""
Law Name: {law.get('law_name')}
Act: {law.get('act')}
Category: {law.get('category')}
Description: {law.get('description')}
"""

    embedding = model.encode(full_text).tolist()

    vectors.append({
        "id": f"law-{i}",
        "values": embedding,
        "metadata": law
    })

# Upload in batches (important)
batch_size = 50

for i in range(0, len(vectors), batch_size):
    batch = vectors[i:i+batch_size]
    index.upsert(vectors=batch)

print("Upload completed successfully.")
