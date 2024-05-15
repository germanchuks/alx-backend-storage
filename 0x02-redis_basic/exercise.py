#!/usr/bin/env python3
"""Module for Cache class"""
import redis
import uuid
from typing import Union, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Counts how many times methods of the Cache class are called."""
    @wraps(method)
    def wrapper_fn(self, *args, **kwargs):
        """Increments the count for a key."""
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper_fn


class Cache:
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Generates a random key, store the input data in Redis using
        the random key and return the key."""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int,
                                                          float]:
        """Getter method"""
        if not self._redis.exists(key):
            return None

        value = self._redis.get(key)
        if fn:
            return fn(value)
        return value

    def get_str(self, key: str) -> str:
        """Get value in string format"""
        return self.get(key, fn=lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """Get value in integer format"""
        return self.get(key, fn=int)
