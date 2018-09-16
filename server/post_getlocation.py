#!/usr/bin/env python3
"""
Implementation for POST request for /getlocation
"""

def handler(database, event):
    try:
        user_id = event["user_id"]
    except KeyError as e:
        return {
            "success": False,
            "failure_reason": str(e),
            "latitude": None,
            "longitude": None,
            "date_created": None
        }

    latitude, longitude, date_created = database.get_last_location(user_id)

    return {
        "success": True,
        "failure_reason": None,
        "latitude": latitude,
        "longitude": longitude,
        "date_created": str(date_created.isoformat())
    }