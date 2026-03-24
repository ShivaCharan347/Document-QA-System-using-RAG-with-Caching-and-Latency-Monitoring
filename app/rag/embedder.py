from sentence_transformers import SentenceTransformer
from app import config
from app.cache.embedding_cache import EmbeddingCache


class Embedder:
    def __init__(self):
        self.model = SentenceTransformer(config.EMBEDDING_MODEL)
        self.cache = EmbeddingCache()

    def embed(self, texts):
        embeddings = []

        for text in texts:
            cached = self.cache.get(text)

            if cached is not None:
                embeddings.append(cached)
                continue

            emb = self.model.encode(text).tolist()
            self.cache.set(text, emb)
            embeddings.append(emb)

        return embeddings