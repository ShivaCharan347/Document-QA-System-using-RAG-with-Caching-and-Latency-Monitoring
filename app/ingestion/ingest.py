from app.ingestion.loader import DocumentLoader
from app.ingestion.chunker import TextChunker
from app.rag.embedder import Embedder
from app.rag.retriever import Retriever
from app import config

class IngestionPipeline:
    def run(self):
        print("Loading documents...")
        docs = DocumentLoader(config.RAW_DATA_PATH).load()
        if not docs:
            print("No documents found.")
            return
            
        print("Chunking...")
        chunks = TextChunker().chunk(docs)
        
        print("Embedding...")
        texts = [c["text"] for c in chunks]
        embeddings = Embedder().embed(texts)
        
        print("Storing in Chroma...")
        retriever = Retriever()
        retriever.store(chunks, embeddings)
        print("Ingestion complete.")
