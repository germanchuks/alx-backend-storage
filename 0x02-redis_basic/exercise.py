#!/usr/bin/env python3
"""Module for Cache class"""
import redis
import uuid
from typing import Union


class Cache:
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Generates a random key, store the input data in Redis using
        the random key and return the key."""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
