import json
import os


CACHE_FILE = os.path.join(os.path.dirname(__file__), "cache.json")

def load_cache():
    """Load the cache from the file. If the file doesn't exist, return an empty dict."""

    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as file:
            return json.load(file)
    return {}


def save_cache(cache):
    """Save the cache dictionary to the cache file."""

    with open(CACHE_FILE, 'w') as file:
        json.dump(cache, file, indent=4)


def get_cache_response(key):
    """
    Retrieves a cached response for a given key..
    """

    cache = load_cache()
    return cache.get(key)


def set_cached_response(key, response):
    """
    Save a response in the cache under the given key.
    """

    cache = load_cache()
    cache[key] = response
    save_cache(cache)


