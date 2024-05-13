#!/usr/bin/env python3
"""Module to insert a new document in a collection"""


def insert_school(mongo_collection, **kwargs):
    """Inserts a new document in a collection"""
    document = mongo_collection.insert_one(kwargs)

    return document.inserted_id
