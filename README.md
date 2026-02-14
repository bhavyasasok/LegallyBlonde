<p align="center">
  <img src="./img.png" alt="Project Banner" width="100%">
</p>

# ForHer ⚖ 

## Basic Details

### Team Name: Glitch

### Team Members
- Member 1: Bhavya S Asok - SCMS School of Engineering and Technology,Palissery,Ernakulam
- Member 2: Surya Kudilil - SCMS School of Engineering and Technology,Palissery,Ernakulam

### Hosted Project Link
[mention your project hosted link here]

### Project Description
A web-based AI legal support assistant that helps women understand their constitutional rights in India. Users can describe their issue in natural language, and the system retrieves relevant Articles from the Constitution of India using Retrieval-Augmented Generation (RAG) and provides structured legal first-aid guidance.

### The Problem statement
Many women in India are unaware of their legal rights or find it difficult to understand complex legal language. Accessing immediate, reliable legal information during distress is challenging, especially without legal consultation or awareness of constitutional protections.

### The Solution
We built an AI-powered legal assistant using Flask and RAG that analyzes a user’s problem, retrieves relevant Articles from the Constitution of India, and generates a simplified explanation along with suggested next steps and helpline information. The system acts as a first-response legal awareness tool, bridging the gap between complex legal documents and real-world problems.

---

## Technical Details

### Technologies/Components Used

**For Software:**

Languages used: Python, HTML, CSS, JavaScript

Frameworks used: Flask

Libraries used:
  OpenAI API (for embeddings & response generation)
  FAISS (for vector similarity search)
  Pandas (for dataset preprocessing)
  NumPy (for numerical operations)

Tools used:
  VS Code
  Git & GitHub
  Kaggle (dataset source)

---

🧠 Core Technology – RAG (Retrieval-Augmented Generation)

Our system uses a RAG pipeline, which combines:

Semantic Retrieval

User input is converted into vector embeddings.

Pinecone vector database retrieves the most relevant legal provisions.

Grounded AI Generation

Retrieved laws are passed to a Large Language Model (Groq LLM).

The LLM generates structured guidance using only the retrieved laws.

This prevents hallucination and ensures legally grounded responses.

## Features

**Feature 1:** AI-Powered Legal Understanding
Users can describe their issue in natural language, and the system interprets the meaning using AI.

**Feature 2:** Retrieval-Augmented Generation (RAG)
The system retrieves relevant Articles from the Constitution of India using semantic search before generating responses.

**Feature 3:** Structured Legal First-Aid Response
The output includes:
  Legal summary
  Applicable Articles
  Immediate next steps
  Emergency helpline numbers
  Disclaimer

**Feature 4:** Mini Chatbot Support
Users can ask follow-up questions for better clarification without re-entering the full problem.

---

## Implementation

### For Software:

#### Installation
```bash
[Installation commands - pip install -r requirements.txt]
```

#### Run
```bash
[Run commands - python app.py]
```


---

## Project Documentation

### For Software:

#### Screenshots (Add at least 3)


Home Page
[Home_page.jpeg](https://github.com/bhavyasasok/LegallyBlonde/blob/main/Home_page.jpeg)

About Page
[About.jpeg](https://github.com/bhavyasasok/LegallyBlonde/blob/main/About_page.jpeg)

Chatbot
[Chatbot.jpeg](https://github.com/bhavyasasok/LegallyBlonde/blob/main/Chatbot.jpeg)

Lawyers Page
[Lawyers_page.jpeg](https://github.com/bhavyasasok/LegallyBlonde/blob/main/Lawyer_page.jpeg)

Demo Video
[ForHerVid.mp4](https://github.com/bhavyasasok/LegallyBlonde/blob/main/ForHerVid%20(1).mp4)

#### Diagrams

**System Architecture:**

Architecture Explanation:

Frontend (HTML, CSS, JavaScript)

Flask Backend (Python)

RAG Pipeline

Embedding Model

Vector Search (FAISS)

Constitution Dataset

OpenAI API for response generation

Structured response sent back to frontend

Data Flow:

User → Frontend → Flask API → RAG Retrieval → OpenAI → Response → Frontend Display
---





## Project Demo

### Video
[video](https://github.com/bhavyasasok/LegallyBlonde/blob/main/ForHerVid%20(1).mp4)
Shows the overall features of the website

---

## AI Tools Used 

Tool Used:
ChatGPT (OpenAI)

Purpose:

Guidance for RAG architecture

Debugging Flask backend

Improving prompt design

Minor UI and documentation assistance

Key Prompts:

“Design a RAG-based legal assistance system.”

“Integrate FAISS with Flask.”

“Improve this legal simplification prompt.”

Approximate AI Contribution:
~25%

Human Contributions:

System architecture and planning

Dataset preparation and embedding setup

Backend and frontend integration

UI/UX design

Testing and optimization
---

## Team Contributions

- [Name 1]: [Specific contributions - e.g., Frontend development, API integration, etc.]
- [Name 2]: [Specific contributions - e.g., Backend development, Database design, etc.]
- [Name 3]: [Specific contributions - e.g., UI/UX design, Testing, Documentation, etc.]

---

## License

This project is licensed under the [LICENSE_NAME] License - see the [LICENSE](LICENSE) file for details.

**Common License Options:**
- MIT License (Permissive, widely used)
- Apache 2.0 (Permissive with patent grant)
- GPL v3 (Copyleft, requires derivative works to be open source)

---

Made with ❤️ at TinkerHub
