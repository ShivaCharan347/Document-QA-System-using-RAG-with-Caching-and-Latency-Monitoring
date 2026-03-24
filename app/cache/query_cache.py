import hashlib

class QueryCache:
    def __init__(self):
        self.cache = {}

    def _key(self, query):
        return hashlib.md5(query.encode()).hexdigest()

    def get(self, query):
        return self.cache.get(self._key(query))

    def set(self, query, response):
        self.cache[self._key(query)] = response