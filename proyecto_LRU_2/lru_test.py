import time
import unittest
from lru_cache import lruCache
from app import fetch_data

class TestLRUCache(unittest.TestCase):
    def test_put_and_get(self):
        cache = lruCache(2)
        cache.put("A", 1)
        cache.put("B", 2)
        self.assertEqual(cache.get("A"), 1)
        self.assertEqual(cache.get("B"), 2)

    def test_eviction(self):
        cache = lruCache(2)
        cache.put("A", 1)
        cache.put("B", 2)
        cache.get("A")  # "A" se usa, "B" será el menos reciente
        cache.put("C", 3)  # "B" se elimina
        self.assertEqual(cache.get("A"), 1)
        self.assertEqual(cache.get("B"), -1)
        self.assertEqual(cache.get("C"), 3)

    def test_update(self):
        cache = lruCache(2)
        cache.put("A", 1)
        cache.put("A", 2)  # Actualiza "A"
        self.assertEqual(cache.get("A"), 2)

class TestAPICachePerformance(unittest.TestCase):
    def test_api_performance(self):
        url = "https://jsonplaceholder.typicode.com/todos/1"
        cache = lruCache(5)

        start = time.perf_counter()
        data1 = fetch_data(url, cache)
        elapsed_first = time.perf_counter() - start

        start = time.perf_counter()
        data2 = fetch_data(url, cache)
        elapsed_second = time.perf_counter() - start

        self.assertEqual(data1, data2)
        self.assertTrue(elapsed_second < elapsed_first, "La segunda llamada no fue más rápida.")

        print(f"\nTiempo de respuesta sin caché: {elapsed_first:.4f} segundos")
        print(f"Tiempo de respuesta con caché: {elapsed_second:.4f} segundos")

if __name__ == "__main__":
    unittest.main()
