Private Context-Restricted AI Chatbot

This project is a Python-based chatbot that acts as a private AI assistant. It allows users to upload custom training data (text or PDF), restricts answers strictly to that content, and simulates email responses using Groq's LLaMA3 large language model via the LangChain framework.

Features

Accepts custom training data (text or PDF)

Strict context-locked responses (no outside knowledge)

Captures user's email and uses name in greetings

Simulates email sending using a send_email() function

Fully interactive UI with Streamlit

Deployed live with public access via Streamlit Cloud

Includes Reset button to clear chat and data completely

Tools & Technologies
Tool/Tech	              Purpose

Python 3.8+	              Core programming language
Streamlit	              Web-based UI framework
Groq API + LLaMA3	      Free LLM via groq client
LangChain	              Retrieval-based QA pipeline
HuggingFace Embeddings	  Text vectorization
FAISS	                  In-memory vector store for similarity
PyPDF2	                  PDF file reading and parsing

File Structure

Private_context_restricted_chatbot/
├── app.py # Streamlit front-end interface
├── chatbot.py # Groq + LangChain logic
├── requirements.txt # Dependencies
├── .gitignore # Prevent secrets from being pushed
├── README.md # This file
└── .streamlit/
  └── secrets.toml # API key (not pushed to GitHub)

 How It Works

User uploads PDF or types training content.

Content is embedded using HuggingFace and stored in FAISS.

On asking a question:

The app searches for relevant content in the FAISS store.

A prompt is sent to Groq LLaMA3 asking it to answer only using the matched content.

If user types “send this to my email” in the query, the app triggers a simulated email response and displays it.

A “Reset” button clears all session data.



Secrets & API Keys

Your Groq API key should be securely stored in:

.streamlit/secrets.toml

Example:

GROQ_API_KEY = "your-groq-api-key-here"

This file is excluded from Git tracking via .gitignore.

Future Improvements

Add real email sending (via SMTP or SendGrid)

Support for additional file types (.docx, .txt)

History tracking of previous conversations

