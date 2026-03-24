import chromadb
from app import config

class Retriever:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=config.CHROMA_PERSIST_DIR)
        self.collection = self.client.get_or_create_collection(config.COLLECTION_NAME)
        
    def store(self, chunks, embeddings):
        ids = [f"chunk_{i}" for i in range(len(chunks))]
        metas = [{"source": c["source"]} for c in chunks]
        docs = [c["text"] for c in chunks]
        
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            metadatas=metas,
            documents=docs
        )
        
    def search(self, query_embedding, k=3):
        results = self.collection.query(query_embeddings=[query_embedding], n_results=k)
        contexts = []
        if results and results["documents"] and results["documents"][0]:
            docs = results["documents"][0]
            metas = results["metadatas"][0] if results["metadatas"] else []
            for i in range(len(docs)):
                contexts.append({
                    "text": docs[i],
                    "source": metas[i].get("source", "unknown") if i < len(metas) else "unknown"
                })
        return contexts
