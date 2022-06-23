cached_results = []

def get_cached_results(query):
    for cache in cached_results:
        if cache["query"] == query:
            print("Found in cache")
            return cache["results"]
    return None

def add_to_cache(query, results):
    cached_results.append({ "query": query, "results": results })