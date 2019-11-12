import logging
from cache.cache_set import CacheSet
from cache.replacement_policy import CacheReplacementPolicy
from cache.replacement_policy import CacheReplacementPolicyLRU

""" N-Way-Associative-Cache in Memory

Basic Usage:
cache = NWayAssociativeCache(num_cache_sets=2, set_size=8)

This will setup a Cache containing two CacheSets (2 ways) each one having a capacity of 8 entries.
By default it will use an LRU policy to evict entries if the cache is full. To use an MRU policy set the 
optional `algo` parameter:

from cache.cache import CacheReplacementPolicyMRU
cache = NWayAssociativeCache(num_cache_sets=2, set_size=8, algo=CacheReplacementPolicyMRU)

"""


class NWayAssociativeCache:
    def __init__(self, num_cache_sets=4, set_size=32, algo=CacheReplacementPolicyLRU):
        """
        Initialize the NWayAssociativeCache
        :param num_cache_sets: number of cache_sets to use
        :param set_size: number of entries for each cache
        :param algo: CacheReplacementPolicy to use
        """
        assert_positive_int(num_cache_sets)
        assert_positive_int(set_size)
        assert_type(algo, CacheReplacementPolicy)
        self.num_cache_sets = num_cache_sets
        self.set_size = set_size
        self.algo = algo
        self.cache_sets = self.__initialize_cache_sets()

    def put(self, key, value):
        """
        Puts a value into the cache. Hashes the key to calculate the index of the cache_set to use.
        If the cache_set is full it selects the entry to remove from the CacheReplacementPolicy algo.
        :param key: key
        :param value: value
        """
        if key is None or value is None:
            raise TypeError

        index = self.__get_cache_set_index(key)
        cache_set = self.cache_sets[index]
        h_key = self.__ensure_hashable_key(key)
        cache_set.put(h_key, value)

    def get(self, key):
        """
        Gets the value for a given key. Hashes the key to calculate the index of the cache_set to use.
        :param key: key
        :return: the Value or None if there is no cache entry for this key
        """
        if key is None:
            raise TypeError

        index = self.__get_cache_set_index(key)
        cache_set = self.cache_sets[index]
        h_key = self.__ensure_hashable_key(key)
        return cache_set.get(h_key)

    def dump(self):
        """
        Dumps all cache entries from all cache_sets
        :return: cache entries from all cache_sets
        """
        for cache_set in self.cache_sets:
            cache_set.dump()

    def __initialize_cache_sets(self):
        logging.info(f'Initializing Cache Sets: num_cache_sets={self.num_cache_sets}')
        cache_sets = [CacheSet(cache_set_id=i, capacity=self.set_size, algo=self.algo())
                      for i in range(self.num_cache_sets)]
        return cache_sets

    def __get_cache_set_index(self, key):
        return abs(self.__hash(key) % self.num_cache_sets)

    def __hash(self, key):
        return hash(self.__ensure_hashable_key(key))

    def __ensure_hashable_key(self, key):
        return frozenset(key) if type(key) == dict or type(key) == list else key


def assert_positive_int(num):
    if isinstance(num, int) and num > 0:
        pass
    else:
        raise ValueError('Invalid int. Expected a positive int value')


def assert_type(clazz, type):
    if issubclass(clazz, type):
        pass
    else:
        raise TypeError(f'Invalid type. Expected object of type {type}')
