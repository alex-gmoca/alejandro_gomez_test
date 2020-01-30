import collections
import time
class cacheLRU:
    def __init__(self, max_capacity, max_age):
        self.max_age = max_age
        self.max_capacity = max_capacity
        self.cache = collections.OrderedDict()

    def get(self, key):
        try:
            item = self.cache.pop(key)
            if (time.time() - item['timestamp']) < self.max_age: 
                self.cache[key] = {
                    "value": item['value'],
                    "timestamp": item['timestamp']
                }
                return item['value']
            return False
        except KeyError:
            return False

    def set(self, key, value):
        try:
            self.cache.pop(key)
        except KeyError:
            if len(self.cache) >= self.max_capacity:
                self.cache.popitem(last=False)
        self.cache[key] = {
            "value": value,
            "timestamp": time.time()
        }
