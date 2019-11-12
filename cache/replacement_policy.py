
from cache.cache_set import CacheSet


class CacheReplacementPolicy:
    def __init__(self):
        dummy = CacheSet.Node()
        self.head = dummy
        self.tail = dummy
        self.head.next = self.tail
        self.tail.previous = self.head

    def node_added(self, node):
        self._add_to_tail(node)

    def node_accessed(self, node):
        self._unlink_node(node)
        self._add_to_tail(node)

    def node_removed(self, node):
        self._unlink_node(node)

    def _add_to_tail(self, node):
        node.previous = self.tail.previous
        node.next = self.tail
        self.tail.previous.next = node
        self.tail.previous = node

    def _unlink_node(self, node):
        node.previous.next = node.next
        node.next.previous = node.previous

    def select(self):
        pass


class CacheReplacementPolicyLRU(CacheReplacementPolicy):
    """
    Default LRU CacheReplacementPolicy
    """
    def select(self):
        return self.head.next if self.head.next != self.tail else None


class CacheReplacementPolicyMRU(CacheReplacementPolicy):
    """
    MRU CacheReplacementPolicy
    """
    def select(self):
        return self.tail.previous if self.tail.previous != self.head else None
