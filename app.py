import streamlit as st
import os
from smart_college_agent import manager_agent, rag_agent, teacher_agent, quiz_agent

st.set_page_config(page_title="Smart College AI Assistant", page_icon="🎓", layout="centered")

# -------------------------
# Animated Background CSS
# -------------------------

st.markdown("""
<style>

/* Animated background */
[data-testid="stAppViewContainer"]{
background: linear-gradient(-45deg,#74ebd5,#ACB6E5,#89f7fe,#66a6ff);
background-size: 400% 400%;
animation: gradientBG 12s ease infinite;
}

/* animation */
@keyframes gradientBG{
0%{background-position:0% 50%;}
50%{background-position:100% 50%;}
100%{background-position:0% 50%;}
}

/* Main card container */
.block-container{
background: rgba(255,255,255,0.75);
padding: 2rem;
border-radius: 18px;
backdrop-filter: blur(8px);
box-shadow: 0px 10px 30px rgba(0,0,0,0.15);
}

/* Title */
h1{
text-align:center;
color:black;
font-weight:700;
}

/* All text black */
.stMarkdown, p, span, label{
color:black !important;
}

/* Input box */
.stTextInput input{
background:white;
color:black;
border-radius:12px;
border:1px solid #ccc;
}

/* Placeholder color */
.stTextInput input::placeholder{
color:black !important;
opacity:0.7;
}

/* Upload box */
.stFileUploader{
background:white;
padding:12px;
border-radius:12px;
}

/* Button */
.stButton>button{
background: linear-gradient(45deg,#667eea,#764ba2);
color:white;
border-radius:30px;
height:3em;
width:180px;
font-weight:600;
border:none;
transition:0.3s;
}

/* Button hover */
.stButton>button:hover{
transform:scale(1.05);
box-shadow:0px 5px 15px rgba(0,0,0,0.3);
}

/* Response box */
.stSuccess{
background:white !important;
color:black !important;
border-radius:12px;
padding:15px;
}

</style>
""", unsafe_allow_html=True)

# -------------------------
# Title
# -------------------------

st.title("🎓 Smart College AI Assistant")

st.markdown(
"""
<center>
Ask questions from your college documents, learn concepts, or generate quizzes instantly.
</center>
""",
unsafe_allow_html=True
)

st.divider()

# -------------------------
# PDF Upload Section
# -------------------------

st.subheader("📄 Upload College Documents")

uploaded_files = st.file_uploader(
    "Upload PDF files",
    type="pdf",
    accept_multiple_files=True
)

if uploaded_files:

    os.makedirs("pdfs", exist_ok=True)

    for file in uploaded_files:
        file_path = os.path.join("pdfs", file.name)

        with open(file_path, "wb") as f:
            f.write(file.getbuffer())

    st.success("✅ PDFs uploaded successfully!")

st.divider()

# -------------------------
# Question Section
# -------------------------

st.subheader("💬 Ask AI")

question = st.text_input("Type your question here")

if st.button("Ask AI 🤖"):

    if question.strip() == "":
        st.warning("Please enter a question.")
        st.stop()

    with st.spinner("🧠 AI is thinking..."):

        decision = manager_agent(question)

        if decision == "RAG":
            result = rag_agent(question)

        elif decision == "QUIZ":
            result = quiz_agent(question)

        else:
            result = teacher_agent(question)

    st.markdown("### 🤖 AI Response")
    st.success(result)