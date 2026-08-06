from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

VECTOR_DB_PATH = "data/chroma_resume_db"
RESUME_PATH = "resumes/master_resume.pdf"

# Local embedding model (free)
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

def load_resume_text():
    """Read text from the resume PDF."""
    reader = PdfReader(RESUME_PATH)
    text = ""

    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"

    print(f"Resume loaded successfully. Characters extracted: {len(text)}")
    return text

def build_resume_vectorstore():
    """Create a Chroma vector database from the resume."""
    resume_text = load_resume_text()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50
    )

    docs = splitter.create_documents([resume_text])

    # Remove old vector database if it exists
    if os.path.exists(VECTOR_DB_PATH):
        import shutil
        shutil.rmtree(VECTOR_DB_PATH)

    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=embedding_model,
        persist_directory=VECTOR_DB_PATH
    )

    print("Vector database created and saved successfully.")
    return vectorstore

def get_resume_retriever():
    """Load the existing Chroma vector database."""
    vectorstore = Chroma(
        persist_directory=VECTOR_DB_PATH,
        embedding_function=embedding_model
    )

    return vectorstore.as_retriever(search_kwargs={"k": 3})

def retrieve_resume_context(query):
    """Retrieve the most relevant resume sections for a query."""
    retriever = get_resume_retriever()
    results = retriever.invoke(query)

    return "\n\n---\n\n".join([doc.page_content for doc in results])

if __name__ == "__main__":
    print("Building resume vector database...")
    build_resume_vectorstore()

    print("\nTesting retrieval...\n")
    context = retrieve_resume_context("FastAPI Docker Python projects")
    print(context)