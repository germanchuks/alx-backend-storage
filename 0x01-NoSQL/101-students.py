#!/usr/bin/env python3
"""Module to retrieve all students sorted by average score"""


def top_students(mongo_collection):
    """Returns all students sorted by average score"""
    students_by_avg_score = mongo_collection.aggregate([
        {
            "$project": {
                "name": "$name",
                "averageScore": {"$avg": "$topics.score"}
            }
        },
        {"$sort": {"averageScore": -1}}
    ])

    return students_by_avg_score
