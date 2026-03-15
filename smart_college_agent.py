
import os
from groq import Groq
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings


# ------------------------
# API
# ------------------------

client = Groq(api_key="Paste your Groq API key here")



# ------------------------
# Load PDFs
# ------------------------

all_docs = []

pdf_folder = "pdfs"

if os.path.exists(pdf_folder):

    for file in os.listdir(pdf_folder):

        if file.endswith(".pdf"):

            loader = PyPDFLoader(os.path.join(pdf_folder, file))
            docs = loader.load()

            all_docs.extend(docs)

print("PDFs Loaded:", len(all_docs))


# ------------------------
# Chunking
# ------------------------

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

chunks = splitter.split_documents(all_docs)


# ------------------------
# Embeddings
# ------------------------

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vector_db = None

if chunks:
    vector_db = FAISS.from_documents(chunks, embedding)
    print("Knowledge Base Ready")
else:
    print("No PDFs found inside 'pdfs' folder")


# ------------------------
# Manager Agent
# ------------------------

def manager_agent(question):

    q = question.lower()

    if "quiz" in q or "mcq" in q:
        return "QUIZ"

    if (
        "rule" in q
        or "policy" in q
        or "attendance" in q
        or "pdf" in q
        or "document" in q
        or "file" in q
        or "summarize" in q
        or "summary" in q
        or "content" in q
    ):
        return "RAG"

    return "TEACH"


# ------------------------
# RAG Agent
# ------------------------

def rag_agent(question):

    if vector_db is None:
        return "No PDFs loaded. Please upload a document first."

    docs = vector_db.similarity_search(question, k=3)

    context = "\n".join([doc.page_content for doc in docs])

    prompt = f"""
Answer strictly from the context below.

Context:
{context}

Question:
{question}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content


# ------------------------
# Teacher Agent
# ------------------------

def teacher_agent(text):

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "Explain simply for engineering students."
            },
            {
                "role": "user",
                "content": text
            }
        ]
    )

    return response.choices[0].message.content


# ------------------------
# Quiz Agent
# ------------------------

def quiz_agent(topic):

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "Generate 5 MCQ questions with answers."
            },
            {
                "role": "user",
                "content": topic
            }
        ]
    )

    return response.choices[0].message.content