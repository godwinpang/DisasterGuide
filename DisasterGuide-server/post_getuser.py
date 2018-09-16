#!/usr/bin/env python3
"""
Implementation for POST request for /getuser
"""

def handler(database, event):
    try:
        user_id = event["user_id"]
    except KeyError as e:
        return {
            "success": False,
            "failure_reason": str(e),
            "first_name": None,
            "last_name": None,
            "age": None,
            "role": None,
            "distress_status": None
        }

    first_name, last_name, age, role = database.get_user_info(user_id)
    distress_status = database.get_distress_status(user_id)

    return {
        "success": True,
        "failure_reason": "None",
        "first_name": first_name,
        "last_name": last_name,
        "age": age,
        "role": role,
        "distress_status": distress_status
    }