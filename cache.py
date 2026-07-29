import os
import pickle


class CacheManager:

    def __init__(self, cache_file):
        self.cache_file = cache_file

    def save(self, data):

        with open(self.cache_file, "wb") as file:
            pickle.dump(data, file)

    def load(self):

        if not self.exists():
            return None

        with open(self.cache_file, "rb") as file:
            return pickle.load(file)

    def exists(self):

        return os.path.exists(self.cache_file)

    def clear(self):

        if self.exists():
            os.remove(self.cache_file)