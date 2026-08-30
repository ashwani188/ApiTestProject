import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
KNOWLEDGE_BASE_DIR = BASE_DIR / "knowledge_base"
CHROMA_DIR = BASE_DIR / "chroma_db"
COLLECTION_NAME = "hr_documents"

# Shared embedding function reused across the module to avoid multiple instantiations
EMBEDDINGS = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


def load_documents():
    if not KNOWLEDGE_BASE_DIR.exists():
        raise FileNotFoundError(f"Knowledge base directory not found: {KNOWLEDGE_BASE_DIR}")

    loader = DirectoryLoader(str(KNOWLEDGE_BASE_DIR), glob="*.txt", loader_cls=TextLoader)
    documents = loader.load()
    if not documents:
        raise ValueError(f"No documents found in {KNOWLEDGE_BASE_DIR}")
    return documents


def build_vector_store():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    documents = load_documents()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(documents)

    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(CHROMA_DIR),
        collection_name=COLLECTION_NAME,
    )

    print(f"Vector store created successfully at: {CHROMA_DIR}")


def get_vector_store():
    # Ensure the persisted vector DB exists; build if missing
    if not CHROMA_DIR.exists():
        build_vector_store()

    return Chroma(
        persist_directory=str(CHROMA_DIR),
        embedding_function=EMBEDDINGS,
        collection_name=COLLECTION_NAME,
    )


def create_rag_chain():
    vector_store = get_vector_store()
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4},
    )
    llm = ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0,
        api_key=os.getenv("GROQ_KEY"),
    )

    rag_prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are an internal HR assistant. Use only the provided context to answer the employee question. "
            "If the answer is missing from the context, say: 'I cannot find that information in the company guidelines.' "
            "Do not invent facts or use outside knowledge.",
        ),
        ("human", "Context:\n{context}\n\nQuestion:\n{question}"),
    ])

    return (
        {"context": retriever, "question": RunnablePassthrough()}
        | rag_prompt
        | llm
        | StrOutputParser()
    )


def ask_question(question: str):
    return create_rag_chain().invoke(question)


def main():
    if not CHROMA_DIR.exists():
        build_vector_store()

    question = input("Enter your question: ").strip()
    if not question:
        print("No question provided.")
        return

    print(f"\nAnswer:\n{ask_question(question)}")


if __name__ == "__main__":
    main()