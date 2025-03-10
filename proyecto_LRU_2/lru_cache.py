from typing import Any, Dict, Optional

class lruNode:
    """Nodo para la caché LRU."""
    def __init__(self, key: Any, value: Any):
        self.key = key
        self.value = value
        self.prev: Optional['lruNode'] = None
        self.next: Optional['lruNode'] = None

class lruCache:
    """Caché LRU con operaciones O(1) usando diccionario y lista doblemente enlazada."""
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache: Dict[Any, lruNode] = {}
        self.head = lruNode(0, 0)
        self.tail = lruNode(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: lruNode) -> None:
        """Elimina un nodo de la lista."""
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _add(self, node: lruNode) -> None:
        """Inserta un nodo al frente (más reciente)."""
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: Any) -> Any:
        """Recupera el valor y lo mueve al frente. Retorna -1 si no existe."""
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            self._add(node)
            return node.value
        return -1

    def put(self, key: Any, value: Any) -> None:
        """Inserta o actualiza un elemento. Elimina el menos usado si se excede la capacidad."""
        if key in self.cache:
            self._remove(self.cache[key])
        new_node = lruNode(key, value)
        self._add(new_node)
        self.cache[key] = new_node

        if len(self.cache) > self.capacity:
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.key]
