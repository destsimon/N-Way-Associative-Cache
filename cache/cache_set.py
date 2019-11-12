import logging
from datetime import datetime
import collections

class CacheSet:
    def __init__(self, cache_set_id, capacity, algo):
        logging.info(f'New Cache Set: cache_set_id={cache_set_id}, capacity={capacity}, algo={algo}')
        self.cache_set_id = cache_set_id
        self.capacity = capacity
        self.algo = algo
        self.cache = {}

    def get(self, key):
        node = self.cache.get(key)
        if node:
            self.__mark_accessed(node)
            return node.value
        else:
            return None

    def put(self, key, value):
        node = self.cache.get(key)
        if not node:
            self.__ensure_capacity()
            self.__add_new(key, value)
        else:
            node.value = value
            self.__mark_accessed(node)

    def get_nodes(self):
        return list(self.cache.values())

    def dump(self):
        for node in self.get_nodes():
            logging.info(f'cache_set[{self.cache_set_id}] node={node}')

    def __add_new(self, key, value):
        new_node = self.Node(key, value)
        self.cache[key] = new_node
        self.algo.node_added(new_node)

    def __mark_accessed(self, node):
        node.last_accessed = datetime.utcnow().timestamp()
        node.hit_count = node.hit_count + 1
        self.algo.node_accessed(node)

    def __ensure_capacity(self):
        while len(self.cache) >= self.capacity:
            node_to_remove = self.algo.select()
            logging.debug(f'Removing Node: {node_to_remove}')
            self.cache.pop(node_to_remove.key, None)
            self.algo.node_removed(node_to_remove)

    class Node:
        def __init__(self, key=None, value=None):
            self.key = key
            self.value = value
            self.last_accessed = datetime.utcnow().timestamp()
            self.hit_count = 1
            self.next = None
            self.previous = None

        def __str__(self):
            last_accessed = datetime.utcfromtimestamp(self.last_accessed)
            return f'key={self.key}, value={self.value}, last_accessed={last_accessed}, hit_count={self.hit_count}'
