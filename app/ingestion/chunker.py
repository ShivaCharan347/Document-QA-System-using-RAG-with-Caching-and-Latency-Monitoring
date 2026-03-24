class TextChunker:
    def __init__(self, chunk_size=600, overlap=100):
        self.size = chunk_size
        self.overlap = overlap
        
    def chunk(self, docs):
        chunks = []
        for doc in docs:
            text = doc["text"]
            start = 0
            while start < len(text):
                end = start + self.size
                chunks.append({
                    "source": doc["source"],
                    "text": text[start:end]
                })
                start = end - self.overlap
        return chunks
