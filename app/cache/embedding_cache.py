import hashlib

class EmbeddingCache:
    def __init__(self):
        self.cache = {}

    def _key(self, text):
        return hashlib.md5(text.encode()).hexdigest()

    def get(self, text):
        return self.cache.get(self._key(text))

    def set(self, text, embedding):
        self.cache[self._key(text)] = embedding