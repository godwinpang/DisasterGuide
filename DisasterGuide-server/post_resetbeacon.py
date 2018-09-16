#!/usr/bin/env python3
"""
Implementation for POST request for /resetbeacon
"""

def handler(database, event):
    try:
        user_id = event["user_id"]
        distress_status = event["distress_status"] if "distress_status" in event else False
    except KeyError as e:
        return {
            "success": False,
            "failure_reason": str(e)
        }

    database.init_distress_status(user_id, distress_status)

    return {
        "success": True,
        "failure_reason": "None"
    }