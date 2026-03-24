import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "db")
COLLECTION_NAME = "rag_docs"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
GROQ_MODEL = "groq/compound-mini"
RAW_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "raw")
