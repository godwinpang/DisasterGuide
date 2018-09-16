#!/usr/bin/env python3
"""
Implementation for POST request for /adddisaster
"""

def handler(database, event):
    try:
        disaster_id = event["disaster_id"]
        disaster_type = event["disaster_type"]
        latitude = event["latitude"]
        longitude = event["longitude"]
        radius = event["radius"]
        severity = event["severity"]
    except KeyError as e:
        return {
            "success": False,
            "failure_reason": str(e)
        }

    database.log_disaster(disaster_id, disaster_type, latitude, longitude, radius, severity)

    return {
        "success": True,
        "failure_reason": "None"
    }