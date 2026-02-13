import json
import numpy as np
import pickle
import faiss
import os
from sentence_transformers import SentenceTransformer

# -------------------------
# CONFIG
# -------------------------
DATA_PATH = "data/women_laws.json"
MODEL_PATH = "model"
INDEX_FILE = os.path.join(MODEL_PATH, "constitution.index")
PICKLE_FILE = os.path.join(MODEL_PATH, "articles.pkl")
EMBED_MODEL_NAME = "all-MiniLM-L6-v2"

# -------------------------
# LOAD JSON DATA
# -------------------------
try:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        laws = json.load(f)

    if not isinstance(laws, list):
        raise ValueError("JSON file must contain a list of laws")

except Exception as e:
    print("❌ Error loading JSON:", str(e))
    exit()

print("✅ JSON loaded successfully")

# -------------------------
# PREPARE DOCUMENTS
# -------------------------
documents = []

for law in laws:
    full_text = f"""
Law Name: {law.get('law_name', '')}
Act: {law.get('act', '')}
Category: {law.get('category', '')}
Description: {law.get('description', '')}
"""

    documents.append({
        "FullText": full_text.strip(),
        "metadata": law  # 🔥 store complete structured law JSON
    })

print("📚 Total laws loaded:", len(documents))

if len(documents) == 0:
    print("❌ No laws found in JSON file")
    exit()

# -------------------------
# LOAD EMBEDDING MODEL
# -------------------------
try:
    print("🔄 Loading embedding model...")
    model = SentenceTransformer(EMBED_MODEL_NAME, local_files_only=True)
    print("✅ Embedding model loaded")
except Exception as e:
    print("❌ Error loading embedding model:", str(e))
    exit()

# -------------------------
# GENERATE EMBEDDINGS
# -------------------------
texts = [doc["FullText"] for doc in documents]

print("🔄 Generating embeddings...")
embeddings = model.encode(texts, show_progress_bar=True)

embeddings = np.array(embeddings).astype("float32")

print("✅ Embeddings generated")

# -------------------------
# BUILD FAISS INDEX
# -------------------------
dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

print("✅ FAISS index built")

# -------------------------
# SAVE INDEX + METADATA
# -------------------------
os.makedirs(MODEL_PATH, exist_ok=True)

faiss.write_index(index, INDEX_FILE)

with open(PICKLE_FILE, "wb") as f:
    pickle.dump(documents, f)

print("💾 Index and metadata saved successfully")
print("🎯 Build complete")
