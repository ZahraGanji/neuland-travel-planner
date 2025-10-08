import os

from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

BOOK_PATH = "data/innocents_abroad_clean.txt"
VECTOR_STORE_PATH = "data/vector_store"


def get_embeddings_model():
    """
    Initializes and returns the Hugging Face embeddings model.
    Returns:
        HuggingFaceEmbeddings: The initialized embeddings model.
    """
    # Using a popular, lightweight, and effective model for embeddings
    model_name = "all-MiniLM-L6-v2"
    return HuggingFaceEmbeddings(model_name=model_name)


def create_vector_store():
    """
    Builds and saves a FAISS vector store from the book text.
    Steps:
    1. Load the book text.
    2. Split the text into smaller chunks.
    3. Create embeddings for each chunk.
    4. Store the embeddings in a FAISS vector database.
    """

    # Load the text from the book file
    if not os.path.exists(BOOK_PATH):
        raise FileNotFoundError(f"Book file not found at: {BOOK_PATH}")
    print("Loading document...")
    loader = TextLoader(BOOK_PATH)
    documents = loader.load()

    # Split document into smaller chunks
    print("Splitting text into chunks...")
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.split_documents(documents)

    # Create embeddings
    print("Initializing Hugging Face embeddings model...")
    embeddings = get_embeddings_model()

    # 4. Create and store in a vector database (FAISS)
    print("Creating vector store...")
    database = FAISS.from_documents(docs, embeddings)

    print("saving vector store...")
    if not os.path.exists(VECTOR_STORE_PATH):
        os.makedirs(VECTOR_STORE_PATH)
    database.save_local(VECTOR_STORE_PATH)
    print("Vector store (FAISS) saved successfully.")


def load_vector_store():
    """
    Loads the FAISS vector store from the local directory.

    Returns:
        FAISS: The loaded vector store object, or None if it doesn't exist.
    """
    if not vector_store_exists():
        raise FileNotFoundError(
            f"Vector store index files were not found in disk. Please create it first."
        )

    print("Loading vector store...")
    embeddings = get_embeddings_model()
    database = FAISS.load_local(
        VECTOR_STORE_PATH, embeddings, allow_dangerous_deserialization=True
    )
    print("Vector store loaded successfully.")
    return database


def vector_store_exists():
    """
    Checks if the FAISS vector store index files exist on disk.


    Returns:
        bool: True if the index exists, False otherwise.
    """
    return os.path.exists(VECTOR_STORE_PATH) and os.path.exists(
        os.path.join(VECTOR_STORE_PATH, "index.faiss")
    )
