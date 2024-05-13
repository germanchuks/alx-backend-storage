#!/usr/bin/env python3
"""Module to change all topics of a school document based on the name"""


def update_topics(mongo_collection, name, topics):
    """Changes all topics of a school document"""
    query = {"name": name}
    newtopics = {"$set": {"topics": topics}}
    mongo_collection.update_many(query, newtopics)
