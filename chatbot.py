import os
import streamlit as st
from groq import Groq
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
import json

# Load Groq key
groq_api_key = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=groq_api_key)

# Simulated email sending function
def send_email(to: str, subject: str, body: str):
    st.info(f"📧 Email to {to}\nSubject: {subject}\nBody:\n{body}")

# Create a vector store retriever
def create_assistant_with_context(context_text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.create_documents([context_text])
    embedding = HuggingFaceEmbeddings()
    db = FAISS.from_documents(docs, embedding)
    retriever = db.as_retriever()
    return retriever

def chat_with_assistant(retriever, question):
    # Extract email first name
    user_email = (
        st.session_state["emails"][0]
        if "emails" in st.session_state and st.session_state["emails"]
        else "user@example.com"
    )
    name_from_email = user_email.split("@")[0].split(".")[0].capitalize()

    # Retrieve relevant docs
    docs = retriever.get_relevant_documents(question)
    context = "\n".join([doc.page_content for doc in docs])

    if not context.strip():
        return f"Hi {name_from_email}, I'm sorry, I can only answer questions based on the provided training content."

    # Check if question asks to send email
    trigger_email = "send this to my email" in question.lower()

    prompt = f"""
You are a strict private assistant.

- Begin all replies with: 'Hi {name_from_email},'
- Only answer based on the context provided.
- If answer is not found in context, say: "I'm sorry, I can only answer questions based on the provided training content."
- If user says "send this to my email", reply normally and trigger a function call.

Context:
{context}

Question:
{question}
"""

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0
    )

    answer = response.choices[0].message.content.strip()

    # Simulate function call
    if trigger_email:
        send_email(user_email, "Response to your query", answer)

    return answer