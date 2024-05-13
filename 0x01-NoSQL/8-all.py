#!/usr/bin/env python3
"""Module to lists all documents in a collection using pymongo"""
from typing import List


def list_all(mongo_collection) -> List[dict]:
    """Lists all documents in a collection"""
    documents = mongo_collection.find()

    if documents.count() == 0:
        return []

    return list(documents)
