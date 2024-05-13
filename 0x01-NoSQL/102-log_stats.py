#!/usr/bin/env python3
"""Retrieves top 10 most presents IPS in the collection `nginx` of the database `logs`"""
from pymongo import MongoClient


if __name__ == "__main__":
    """Provides stats about Nginx logs stored in MongoDB"""
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx

    number_of_logs = nginx_collection.count_documents({})
    print(f'{number_of_logs} logs')

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print('Methods:')
    for method in methods:
        count = nginx_collection.count_documents({"method": method})
        print(f'\tmethod {method}: {count}')

    status_check = nginx_collection.count_documents({"method": "GET",
                                                     "path": "/status"})

    print(f'{status_check} status check')

    top_IPS = nginx_collection.aggregate([
        {"$group":
            {
                "_id": "$ip",
                "count": {"$sum": 1}
            }
         },
        {"$sort": {"count": -1}},
        {"$limit": 10},
        {"$project": {
            "_id": 0,
            "ip": "$_id",
            "count": 1
        }}
    ])

    print("IPs:")
    for top_IP in top_IPS:
        ip = top_IP.get("ip")
        count = top_IP.get("count")
        print(f'\t{ip}: {count}')
