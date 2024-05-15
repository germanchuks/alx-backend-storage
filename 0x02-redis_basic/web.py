#!/usr/bin/env python3
"""Module to get HTML content of an URL"""
from functools import wraps
import redis
import requests
from typing import Callable


redis_ = redis.Redis()


def count_requests(method: Callable) -> Callable:
    """Counts how many times an URL is accessed and cache result with
    expiration time of 10 seconds"""
    @wraps(method)
    def wrapper_fn(url):
        redis_.incr(f"count:{url}")
        cached_content = redis_.get(f"cached:{url}")
        if cached_content:
            return cached_content.decode('utf-8')
        page = method(url)
        redis_.setex(f"cached:{url}", 10, page)
        return page

    return wrapper_fn


@count_requests
def get_page(url: str) -> str:
    """Obtains and returns HTML content of a particular URL using
    requests module."""
    request = requests.get(url)
    return request.text
