import os
from geoloc_util import cache


def test_load_cache_empty(temp_cache_file):
    """
    Test that load_cache() returns an empty dictionary
    when the cache file does not exist.
    """

    loaded = cache.load_cache()
    assert loaded == {}, "Expected an empty dictionary when the cache file does not exist"


def test_set_and_get_cached_response(temp_cache_file):
    """
    Test that set_cached_response() properly saves data,
    and get_cache_response() retrieves the same data.
    """

    key = 'test_key'
    response = {"data": "value"}

    cache.set_cached_response(key, response)
    loaded_response = cache.get_cache_response(key)
    assert loaded_response == response, 'Expected the cached response to match the set value.'

    assert os.path.exists(temp_cache_file), "Expected the cache file to be created."


def test_save_and_load_cache(temp_cache_file):
    """
    Test that save_cache() correctly writes data to the file
    and load_cache() returns the same data.
    """

    data = {"key1": "value1", "key2": 2}
    cache.save_cache(data)
    loaded_data = cache.load_cache()

    assert loaded_data == data, "Expected loaded cache data to match the saved data."

