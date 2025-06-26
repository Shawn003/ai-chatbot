import streamlit as st
from PyPDF2 import PdfReader
from chatbot import create_assistant_with_context, chat_with_assistant

st.set_page_config(page_title="AI Chatbot", page_icon="🤖")
st.title("🤖 Private AI Chatbot")

st.markdown("### 📚 Training Data (Type or Attach PDF)")
st.markdown("""
<style>
[data-testid="stFileUploaderDropzone"] > div:first-child {
    display: none;
}
.file-upload-container {
    position: relative;
    top: -36px;
    float: right;
    margin-right: 10px;
}
</style>
""", unsafe_allow_html=True)

# Input area
context_text = st.text_area(" ", placeholder="Paste your training content here...", height=250, label_visibility="collapsed")

with st.container():
    st.markdown('<div class="file-upload-container">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(" ", type=["pdf"], label_visibility="collapsed", key="file_uploader")
    st.markdown('</div>', unsafe_allow_html=True)

# Save Context
if st.button("💾 Save Context"):
    if uploaded_file and not context_text.strip():
        try:
            reader = PdfReader(uploaded_file)
            extracted = "".join(page.extract_text() or "" for page in reader.pages)
            st.session_state["training_data"] = extracted
            st.success("✅ PDF content extracted and saved.")
        except Exception as e:
            st.error(f"❌ Failed to read PDF: {e}")
    elif context_text.strip():
        st.session_state["training_data"] = context_text
        st.success("✅ Training content saved successfully.")
    else:
        st.warning("⚠️ Please either upload a PDF or enter text.")

# Email input
st.subheader("📧 Email Address ")
email = st.text_input("Enter your email")
if email:
    if "emails" not in st.session_state:
        st.session_state["emails"] = []
    if email not in st.session_state["emails"]:
        st.session_state["emails"].append(email)

# Question input
st.subheader("💬 Ask a Question")
question = st.text_input("Type your question here")

col1, col2 = st.columns([6, 1])
with col1:
    ask_clicked = st.button("Ask", use_container_width=True)
with col2:
    reset_clicked = st.button("🔄 Reset", use_container_width=True)

# Reset logic
if reset_clicked:
    for key in ["qa", "training_data", "emails", "file_uploader", "question"]:
        if key in st.session_state:
            del st.session_state[key]
    with st.spinner("♻️ Resetting chatbot..."):
        import time
        time.sleep(1.2)
        st.markdown('<meta http-equiv="refresh" content="0">', unsafe_allow_html=True)

# Chat logic
if ask_clicked:
    if "training_data" not in st.session_state or not st.session_state["training_data"].strip():
        st.warning("⚠️ Please save your training content first.")
    elif not question.strip():
        st.warning("❗ Please enter a valid question.")
    else:
        with st.spinner("🤖 Generating answer..."):
            try:
                if "qa" not in st.session_state:
                    st.session_state["qa"] = create_assistant_with_context(st.session_state["training_data"])
                answer = chat_with_assistant(st.session_state["qa"], question)
                st.success("🧠 AI Response:")
                st.write(answer)
            except Exception as e:
                st.error(f"❌ Error: {e}")
