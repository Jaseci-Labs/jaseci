class MockRedis:
    def __init__(self, cache=dict()):
        self.cache = cache

    def get(self, key):
        if key in self.cache:
            return self.cache[key]
        return None  # return nil

    def set(self, key, value, *args, **kwargs):
        self.cache[key] = value
        return "OK"

    def hget(self, hash, key):
        if hash in self.cache:
            if key in self.cache[hash]:
                return self.cache[hash][key]
        return None  # return nil

    def hset(self, hash, key, value, *args, **kwargs):
        self.cache[hash][key] = value
        return 1

    def exists(self, key):
        if key in self.cache:
            return 1
        return 0

    def delete(self, key):
        del self.cache[key]
        return None  # return nil

    def cache_overwrite(self, cache=dict()):
        self.cache = cache
