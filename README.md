<p align="center">
  <img src="./img.png" alt="Project Banner" width="100%">
</p>

# ForHer ⚖

AI-Powered Legal First-Aid for Women in India

---

# Basic Details

### Team Name:

Glitch

### Team Members

* **Bhavya S Asok** – SCMS School of Engineering and Technology, Palissery, Ernakulam
* **Surya Kudilil** – SCMS School of Engineering and Technology, Palissery, Ernakulam


---

# Project Description

ForHer is a web-based AI legal support assistant that helps women understand their legal rights in India.

Users describe their issue in natural language, and the system uses **Retrieval-Augmented Generation (RAG)** to retrieve relevant laws and generate structured legal first-aid guidance.

The platform simplifies complex legal language into understandable advice while strictly grounding responses in actual legal provisions.

---

# Problem Statement

Many women in India:

* Are unaware of their legal rights
* Struggle to interpret complex legal language
* Cannot access immediate legal consultation during distress
* Need quick, reliable legal awareness support

Accessing legal help quickly and safely is often difficult.

---

# Our Solution

We built an AI-powered legal assistant that:

1. Accepts natural language legal problems
2. Retrieves relevant Indian laws using semantic search
3. Uses RAG (Retrieval-Augmented Generation) to ensure grounded responses
4. Generates structured legal first-aid guidance
5. Provides emergency helpline support

The system bridges the gap between:

Legal Documents → Real-World Problems

---

# Key Features

### 1️⃣ AI-Powered Legal Understanding

Users describe their issue in natural language. The system interprets intent using embeddings.

---

### 2️⃣ Retrieval-Augmented Generation (RAG)

Instead of letting the AI guess:

* The user input is converted into embeddings
* Pinecone retrieves relevant laws
* Groq LLM generates explanation strictly based on retrieved laws

This prevents hallucination.

---

### 3️⃣ Structured Legal First-Aid Response

Each response includes:

* Related Laws (ID, Act, Category, Emergency flag, Description)
* What the Law Says
* Next Steps
* Emergency Helplines
* Legal Disclaimer

---

### 4️⃣ Mini Chatbot Support

Users can ask follow-up clarification questions without re-entering their full issue.

---

# Technical Details

## Technologies Used

### Backend

* Python
* Flask
* Groq LLM (LLaMA 3.1)
* Pinecone (Vector Database)
* Sentence Transformers (HuggingFace)

### Frontend

* HTML
* CSS
* JavaScript

### Tools

* VS Code
* Git & GitHub
* Kaggle (Dataset Source)
* Render (Deployment)

---

# RAG Architecture

## Data Flow

User → Frontend → Flask API → Embedding → Pinecone Retrieval → Groq → Structured JSON → Frontend Display

---

# API Documentation

## Base URL

```
http://localhost:5001
```

Production:

```
https://your-render-link.onrender.com
```

---

## POST /analyze

### Description

Analyzes user problem using RAG pipeline and returns structured legal response.

### Request

```json
{
  "problem": "My husband is demanding dowry and threatening me"
}
```

### Response

```json
{
  "related_laws": [
    {
      "law_id": "BNS-64",
      "law_name": "Punishment for Rape",
      "act": "Bharatiya Nyaya Sanhita 2023",
      "category": "Sexual Offence",
      "description": "Specifies punishment for rape.",
      "emergency": true,
      "severity_level": 10,
      "gender_specific": true
    }
  ],
  "what_the_law_says": "...",
  "your_next_steps": "...",
  "helplines": "112, 181",
  "disclaimer": "This is informational only."
}
```

---

## POST /chat

### Description

Handles follow-up questions.

### Request

```json
{
  "message": "What evidence do I need?"
}
```

### Response

```json
{
  "response": "You may collect documentary and testimonial evidence..."
}
```

---

# Installation Guide

## 1️⃣ Clone Repository

```
git clone https://github.com/bhavyasasok/LegallyBlonde.git
cd ForHer
```

---

## 2️⃣ Create Virtual Environment

```
python -m venv .venv
source .venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```
pip install -r requirements.txt
```

---

## 4️⃣ Add Environment Variables

Create `.env` file:

```
GROQ_API_KEY=your_groq_key
PINECONE_API_KEY=your_pinecone_key
```

---

## 5️⃣ Run Server

```
python app.py
```

Open:

```
http://localhost:5001
```

---

# Screenshots

Home Page
[https://github.com/bhavyasasok/LegallyBlonde/blob/main/Home_page.jpeg](https://github.com/bhavyasasok/LegallyBlonde/blob/main/Home_page.jpeg)

About Page
[https://github.com/bhavyasasok/LegallyBlonde/blob/main/About_page.jpeg](https://github.com/bhavyasasok/LegallyBlonde/blob/main/About_page.jpeg)

Chatbot
[https://github.com/bhavyasasok/LegallyBlonde/blob/main/Chatbot.jpeg](https://github.com/bhavyasasok/LegallyBlonde/blob/main/Chatbot.jpeg)

Lawyers Page
[https://github.com/bhavyasasok/LegallyBlonde/blob/main/Lawyer_page.jpeg](https://github.com/bhavyasasok/LegallyBlonde/blob/main/Lawyer_page.jpeg)

---

# Demo Video

[https://github.com/bhavyasasok/LegallyBlonde/blob/main/ForHerVid%20(1).mp4](https://github.com/bhavyasasok/LegallyBlonde/blob/main/ForHerVid%20%281%29.mp4)

---

# AI Tools Used

Tool:
ChatGPT (OpenAI)

Purpose:

* RAG architecture guidance
* Flask debugging
* Prompt engineering refinement
* Documentation assistance

Approximate AI Contribution:
~25%

Human Contribution:

* System architecture
* Dataset preparation
* Pinecone indexing
* Backend logic
* Frontend integration
* UI/UX design
* Testing & optimization

---

# Team Contributions

### Bhavya S Asok

* Backend development
* RAG implementation
* Pinecone integration
* API design
* Deployment setup

### Surya Kudilil

* Frontend development
* UI/UX design
* Chatbot integration
* Testing and debugging
* Documentation

---

# License

This project is licensed under the MIT License.

---

# Safety Disclaimer

This platform provides informational legal guidance only.

It does not replace consultation with a qualified legal professional.

Emergency Contacts:

* 112 – National Emergency
* 181 – Women Helpline

---

Made with ❤️ at TinkerHub

---


