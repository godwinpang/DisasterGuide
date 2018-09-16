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
    except KeyError as e:
        return {
            "success": False,
            "failure_reason": str(e)
        }

    database.add_user(first_name, last_name, date(birthday["year"], birthday["month"], birthday["day"]), user_id)

    return {
        "success": True,
        "failure_reason": "None"
    }