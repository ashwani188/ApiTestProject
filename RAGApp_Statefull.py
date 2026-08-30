
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
KNOWLEDGE_BASE_DIR = BASE_DIR / "knowledge_base"
CHROMA_DIR = BASE_DIR / "chroma_db"
MEMORY_DB = BASE_DIR / "conversation_memory.db"
COLLECTION_NAME = "hr_documents"


def init_memory_db():
    conn = sqlite3.connect(MEMORY_DB)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS conversation_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    conn.close()


def save_conversation_turn(session_id: str, question: str, answer: str):
    init_memory_db()
    conn = sqlite3.connect(MEMORY_DB)
    conn.execute(
        "INSERT INTO conversation_memory (session_id, question, answer) VALUES (?, ?, ?)",
        (session_id, question.strip(), str(answer).strip()),
    )
    conn.commit()
    conn.close()


def get_recent_memory(session_id: str, limit: int = 5):
    init_memory_db()
    conn = sqlite3.connect(MEMORY_DB)
    rows = conn.execute(
        "SELECT question, answer FROM conversation_memory WHERE session_id = ? ORDER BY id DESC LIMIT ?",
        (session_id, limit),
    ).fetchall()
    conn.close()
    memory_entries = []
    for question, answer in reversed(rows):
        memory_entries.append(f"Q: {question}\nA: {answer}")
    return "\n\n".join(memory_entries) if memory_entries else "No previous conversation for this session."


def document_loader():
    return DirectoryLoader(str(KNOWLEDGE_BASE_DIR), glob="*.txt", loader_cls=TextLoader).load()


def embeddings(documents):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    chunks = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50).split_documents(documents)
    return Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(CHROMA_DIR),
        collection_name=COLLECTION_NAME,
    )


def _save_chat_to_kb(question: str, answer: str):
    """Save chat into the knowledge_base as a new file and return the path."""
    KNOWLEDGE_BASE_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = KNOWLEDGE_BASE_DIR / f"chat_{timestamp}.txt"
    with open(path, "w", encoding="utf-8") as f:
        f.write("User: " + question.strip() + "\n\n")
        f.write("Assistant: " + str(answer).strip() + "\n")
    return path


def ask_question(vector_store, question: str, session_id: str = "default"):
    llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0.7, api_key=os.getenv("GROQ_KEY"))

    retriever = vector_store.as_retriever(search_kwargs={"k": 2})
    docs = retriever.invoke(question)
    context = "\n\n".join(doc.page_content for doc in docs) if docs else "No relevant knowledge found."
    memory = get_recent_memory(session_id, limit=5)

    prompt = ChatPromptTemplate.from_template(
        "You are a helpful assistant. Use the previous conversation and the retrieved knowledge to answer the user.\n\n"
        "Previous conversation:\n{memory}\n\n"
        "Relevant knowledge:\n{context}\n\n"
        "Question: {question}\n\nAnswer:"
    ).format(memory=memory, context=context, question=question)

    response = llm.invoke(prompt)
    return response.content


def main():
    KNOWLEDGE_BASE_DIR.mkdir(parents=True, exist_ok=True)
    documents = document_loader()
    vector_store = embeddings(documents)

    session_id = input("Session ID (press Enter for default): ").strip() or "default"
    question = input("Enter a question: ").strip()
    if not question:
        print("No question provided.")
        return

    try:
        answer = ask_question(vector_store, question, session_id=session_id)
    except Exception as e:
        print(f"Error during retrieval/LLM call: {e}")
        return

    print(f"\nAnswer:\n{answer}")

    try:
        save_conversation_turn(session_id, question, answer)
        _save_chat_to_kb(question, answer)
        embeddings(document_loader())
    except Exception:
        pass


if __name__ == "__main__":
    main()