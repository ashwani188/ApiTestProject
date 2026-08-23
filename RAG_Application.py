import os
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

def main():
    print("--- Step 1: Loading Documents ---")
    # loader= DirectoryLoader("knowledge_base", glob="**/*.txt")
    loader = DirectoryLoader("./knowledge_base", glob="*.txt", loader_cls=TextLoader)
    raw_documents = loader.load()
    print(f"Loaded {len(raw_documents)} raw document source file(s).")

    print("\n--- Step 2: Splitting Documents into Chunks ---")
    # Split text into bite-sized segments so the retriever can pin down specific paragraphs
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,  # Number of characters per chunk
        chunk_overlap=50  # Overlap to preserve context across chunks
    )
    chunks = text_splitter.split_documents(raw_documents)
    print(f"Created {len(chunks)} text chunks.")

    print("\n--- Step 3: Initializing Embeddings & Vector Database ---")
    # This model runs 100% locally on your machine to convert words into numeric vector grids
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Save the vector index directly in an in-memory database configuration
    vector_store = Chroma.from_documents(chunks, embeddings)
    # Configure it to act as a retriever that fetches the top 2 closest context blocks
    retriever = vector_store.as_retriever(search_kwargs={"k": 2})
    print("Vector database built and configured successfully.")

    print("\n--- Step 4: Building the LLM and Prompt Strategy ---")
    # Connect your live Groq token to the active standard engine
    llm= init_chat_model(model="openai/gpt-oss-20b", model_provider="groq", api_key=os.getenv("GROQ_KEY"))

    rag_prompt = ChatPromptTemplate.from_messages([
        ("system", (
            "You are an internal corporate HR assistant.\n"
            "Answer the employee question using ONLY the provided context below.\n"
            "If you do not know the answer or if it's missing from the context, "
            "say 'I cannot find that information in the company guidelines.' Do not invent facts.\n\n"
            "CONTEXT:\n{context}"
        )),
        ("human", "{question}")
    ])

    print("\n--- Step 5: Assembling the LCEL RAG Chain ---")
    # Combine individual operations into a unified functional stream
    rag_chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | rag_prompt
            | llm
            | StrOutputParser()
    )
    print("RAG execution engine pipeline ready.")

    print("\n--- Step 6: Testing the Application ---")
    # Run a test question
    query = "Is there any Stipend?"
    print(f"Question: {query}\n")

    response = rag_chain.invoke(query)
    print("Answer:"+ response)


if __name__ == "__main__":
    main()