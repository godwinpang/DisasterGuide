#!/usr/bin/env python3
"""
Implementation for POST request for /getlocationhistory
"""

def handler(database, event):
    try:
        user_id = event["user_id"]
    except KeyError as e:
        return {
            "success": False,
            "failure_reason": str(e),
            "location": None,
            "date_created": None
        }

    past_locations = database.get_past_locations(user_id)

    return {
        "success": True,
        "failure_reason": "None",
        "locations": [{"latitude": tp[0], "longitude": tp[1], "date_created": tp[2].isoformat()} for tp in past_locations]
    }