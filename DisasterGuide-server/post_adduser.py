#!/usr/bin/env python3
"""
Implementation for POST request for /adduser
"""

from datetime import date

def handler(database, event):
    try:
        user_id = event["user_id"] if "user_id" in event else None
        first_name = event["first_name"]
        last_name = event["last_name"]
        birthday = event["birthday"]
        role = event["role"]
    except KeyError as e:
        return {
            "success": False,
            "user_id": None,
            "failure_reason": str(e)
        }

    user_id = database.add_user(first_name, last_name, date(birthday["year"], birthday["month"], birthday["day"]), role, user_id)
    database.init_distress_status(user_id)

    return {
        "success": True,
        "user_id": user_id,
        "failure_reason": "None"
    }