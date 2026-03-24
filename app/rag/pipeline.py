from app.rag.embedder import Embedder
from app.rag.retriever import Retriever
from app.rag.prompt import build_prompt
from app.llm.groq_client import GroqClient
from app.cache.query_cache import QueryCache
from app.monitoring.metrics import Timer
from app.monitoring.logger import logger


class RAGPipeline:
    def __init__(self):
        self.embedder = Embedder()
        self.retriever = Retriever()
        self.llm = GroqClient()
        self.cache = QueryCache()

    def run(self, query):
        logger.info(f"Query received: {query}")

        # ✅ Cache check
        cached = self.cache.get(query)
        if cached:
            logger.info("Cache hit")
            return cached

        total_timer = Timer()

        # ✅ Embedding + Retrieval
        t1 = Timer()
        q_embed = self.embedder.embed([query])[0]
        contexts = self.retriever.search(q_embed)
        retrieval_time = t1.stop()

        if not contexts:
            return {
                "answer": "No relevant documents found.",
                "sources": [],
                "latency": {}
            }

        logger.info(f"Retrieved {len(contexts)} chunks")

        # ✅ Generation
        t2 = Timer()
        prompt = build_prompt(query, contexts)
        answer = self.llm.generate(prompt)
        generation_time = t2.stop()

        sources = list(set([c["source"] for c in contexts]))

        total_time = total_timer.stop()

        result = {
            "answer": answer,
            "sources": sources,
            "latency": {
                "retrieval": retrieval_time,
                "generation": generation_time,
                "total": total_time
            }
        }

        # ✅ Store in cache
        self.cache.set(query, result)

        logger.info(f"Total latency: {total_time}s")

        return result