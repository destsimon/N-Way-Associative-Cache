
import unittest
import threading

from cache.cache import NWayAssociativeCache
from cache.replacement_policy import CacheReplacementPolicy, CacheReplacementPolicyLRU, CacheReplacementPolicyMRU


class TestCache(unittest.TestCase):
    def setUp(self):
        pass

    def test_cache_lru(self):
        cache = NWayAssociativeCache(num_cache_sets=2, set_size=8, algo=CacheReplacementPolicyLRU)

        for i in range(20):
            cache.put(i, i)

        for i in range(4, 20):
            self.assertEqual(i, cache.get(i))

    def test_cache_mru(self):
        cache = NWayAssociativeCache(num_cache_sets=2, set_size=8, algo=CacheReplacementPolicyMRU)

        for i in range(20):
            cache.put(i, i)

        # first 14 elements are the 14 least accessed items
        for i in range(14):
            self.assertEqual(i, cache.get(i))

        # the last two entries are the MRU entries that have the latest added key/values
        self.assertEqual(18, cache.get(18))
        self.assertEqual(19, cache.get(19))

    def test_cache_custom(self):
        class CustomCacheReplacementPolicy(CacheReplacementPolicy):
            @staticmethod
            def select(cache_set):
                nodes = cache_set.get_nodes()
                remove_node = nodes[-1]
                return remove_node

        cache = NWayAssociativeCache(num_cache_sets=2, set_size=8, algo=CustomCacheReplacementPolicy)

        for i in range(16):
            cache.put(i, i)

        for i in range(16):
            self.assertEqual(i, cache.get(i))

    def test_cache_capacity(self):
        cache = NWayAssociativeCache(num_cache_sets=2, set_size=8)

        for i in range(100):
            cache.put(i, i)

        for cache_block in cache.cache_sets:
            self.assertEqual(8, len(cache_block.cache))

    def test_cache_multiple_threads(self):
        def put_cache(c, start, end):
            for i in range(start, end):
                c.put(i, i)

        cache = NWayAssociativeCache(num_cache_sets=2, set_size=8)

        t1 = threading.Thread(target=put_cache, args=(cache, 0, 50))
        t2 = threading.Thread(target=put_cache, args=(cache, 25, 75))

        t1.start()
        t2.start()

        t1.join()
        t2.join()

        for cache_set in cache.cache_sets:
            self.assertEqual(8, len(cache_set.cache))

    def test_cache_value_error(self):
        try:
            cache = NWayAssociativeCache(num_cache_sets=-1)
        except ValueError:
            return

        self.fail('expected ValueError')

    def test_cache_type_error(self):
        try:
            cache = NWayAssociativeCache(algo={})
        except TypeError:
            return

        self.fail('expected TypeError')
