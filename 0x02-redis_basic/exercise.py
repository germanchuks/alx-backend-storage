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


def call_history(method: Callable) -> Callable:
    """Stores the history of inputs and outputs for a particular function."""
    @wraps(method)
    def wrapper_fn(self, *args, **kwargs):
        inputs_key = f"{method.__qualname__}:inputs"
        outputs_key = f"{method.__qualname__}:outputs"

        self._redis.rpush(inputs_key, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(outputs_key, output)
        return output
    return wrapper_fn


def replay(method: Callable) -> None:
    """Displays the history of calls of a particular function."""
    inputs_key = f"{method.__qualname__}:inputs"
    outputs_key = f"{method.__qualname__}:outputs"

    cache = redis.Redis()
    inputs = cache.lrange(inputs_key, 0, -1)
    outputs = cache.lrange(outputs_key, 0, -1)

    print(f"Cache.{method.__name__} was called {len(inputs)} times:")
    for input_args, output in zip(inputs, outputs):
        print(f"Cache.{method.__name__}(*{input_args.decode("utf-8")}) -> {\
            output.decode("utf-8")}")


class Cache:
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
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
