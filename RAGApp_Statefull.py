
import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

load_dotenv()

def document_loader():
    return DirectoryLoader("./knowledge_base", glob="*.txt", loader_cls=TextLoader).load()

def embeddings(documents):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    chunks=RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50).split_documents(documents)
    return Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="./chroma_db",
        collection_name="hr_documents")

def _save_chat_to_kb(question: str, answer: str):
    """Save chat into the knowledge_base as a new file and return the path."""
    kb_dir = Path("./knowledge_base")
    kb_dir.mkdir(parents=True, exist_ok=True)
    import datetime

    timestamp = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    fname = f"chat_{timestamp}.txt"
    path = kb_dir / fname
    with open(path, "w", encoding="utf-8") as f:
        f.write("User: " + question.strip() + "\n\n")
        f.write("Assistant: " + str(answer).strip() + "\n")
    return path


def ask_question(vector_store, question):
    # Use ChatGroq via langchain_groq
    llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0.7, api_key=os.getenv("GROQ_KEY"))
    prompt_template = ChatPromptTemplate.from_template(
        "You are a helpful assistant. Use the following context to answer the question.\n\n{context}\n\nQuestion: {question}\nAnswer:"
    )
    retriever = vector_store.as_retriever(search_kwargs={"k": 2})
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt_template
        | llm
        | StrOutputParser()
    )
    return chain.invoke(question)


def main():
    documents = document_loader()
    vector_store = embeddings(documents)
    question = input("Enter a question: ").strip()
    if not question:
        print("No question provided.")
        return
    try:
        answer = ask_question(vector_store, question)
    except Exception as e:
        print(f"Error during retrieval/LLM call: {e}")
        return

    print(f"\nAnswer:\n{answer}")

    # Persist this chat into the KB so future queries can retrieve it
    try:
        _save_chat_to_kb(question, answer)
        # Rebuild vector store to include the new chat
        embeddings(document_loader())
    except Exception:
        pass



if __name__ == "__main__":
    main()