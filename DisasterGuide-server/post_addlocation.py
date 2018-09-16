#!/usr/bin/env python3
"""
Implementation for POST request for /addlocation
"""

def handler(database, event):
    try:
        user_id = event["user_id"]
        latitude = event["latitude"]
        longitude = event["longitude"]
    except KeyError as e:
        return {
            "success": False,
            "failure_reason": str(e)
        }

    database.log_location(user_id, latitude, longitude)

    return {
        "success": True,
        "failure_reason": "None"
    }