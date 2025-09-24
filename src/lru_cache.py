# /src/lru_cache.py

class _Node:
    __slots__ = ("key", "val", "prev", "next")

    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, capacity):
        assert capacity > 0
        self.cap = capacity
        self.map = {}  # key -> node
        # sentinels
        self.head = _Node("__H__", None)  # most recent after head
        self.tail = _Node("__T__", None)  # least recent before tail
        self.head.next = self.tail
        self.tail.prev = self.head

    # helper to remove a node from linked list
    def _remove(self, node):
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    # helper to insert node right after head (most recent)
    def _insert_at_head(self, node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key):
        if key not in self.map:
            return None
        node = self.map[key]
        # move to head (most recent)
        self._remove(node)
        self._insert_at_head(node)
        return node.val

    def put(self, key, val):
        if key in self.map:
            node = self.map[key]
            node.val = val
            self._remove(node)
            self._insert_at_head(node)
        else:
            if len(self.map) >= self.cap:
                # evict least recent (node before tail)
                lru = self.tail.prev
                self._remove(lru)
                del self.map[lru.key]
            node = _Node(key, val)
            self.map[key] = node
            self._insert_at_head(node)
