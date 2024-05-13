#!/usr/bin/env python3
"""Module to retrieve the list of school having a specific topic"""


def schools_by_topic(mongo_collection, topic):
    """Returns the list of school having a specific topic"""
    query = {"topics": topic}
    documents = mongo_collection.find(query)
    return documents
