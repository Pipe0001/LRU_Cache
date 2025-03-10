import requests
from lru_cache import lruCache

def fetch_data(url: str, cache: lruCache) -> dict:
    """
    Intenta obtener la respuesta de la API desde la caché.
    Si no está en caché, hace una petición y la almacena.
    """
    cached_response = cache.get(url)
    if cached_response != -1:
        print(f"[CACHE HIT] {url}")
        return cached_response
    else:
        print(f"[CACHE MISS] {url} - realizando petición a la API...")
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            cache.put(url, data)
            return data
        else:   
            response.raise_for_status()

if __name__ == "__main__":
    cache = lruCache(3)

    # Pruebas manuales de la caché
    print("Agregando A=1")
    cache.put("A", 1)
    print("Agregando B=2")
    cache.put("B", 2)
    print("Recuperando A:", cache.get("A"))
    print("Agregando C=3")
    cache.put("C", 3)
    print("Agregando D=4 (debe eliminar B)")
    cache.put("D", 4)
    print("Recuperando B:", cache.get("B"))
    print("Recuperando C:", cache.get("C"))

    # Prueba con API
    url = "https://jsonplaceholder.typicode.com/todos/1"
    print("Haciendo primera petición a la API...")
    data1 = fetch_data(url, cache)
    print("Haciendo segunda petición (debe venir de la caché)...")
    data2 = fetch_data(url, cache)

    print("Datos de la API (primer intento):", data1)
    print("Datos de la API (segundo intento):", data2)

