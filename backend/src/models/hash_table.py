from typing import Any, List, Optional, Tuple


class HashTable:
    """A hash table implementation with collision handling."""

    def __init__(self, size: int = 100):
        self.size = size
        self.table: List[List[Tuple[Any, Any]]] = [[] for _ in range(size)]

    def _hash(self, key: Any) -> int:
        return hash(key) % self.size

    def insert(self, key: Any, value: Any) -> None:
        index = self._hash(key)
        for kvp in self.table[index]:
            if kvp[0] == key:
                kvp[1] = value
                return
        self.table[index].append([key, value])

    def get(self, key: Any) -> Optional[Any]:
        index = self._hash(key)
        for kvp in self.table[index]:
            if kvp[0] == key:
                return kvp[1]
        return None

    def delete(self, key: Any) -> None:
        index = self._hash(key)
        for i, kvp in enumerate(self.table[index]):
            if kvp[0] == key:
                del self.table[index][i]
                return

    def __len__(self) -> int:
        return sum(len(bucket) for bucket in self.table)

    def items(self) -> List[Tuple[Any, Any]]:
        """Returns all key-value pairs in the hash table."""
        items = []
        for bucket in self.table:
            items.extend(bucket)
        return items
