#!/usr/bin/env python3
"""
Implementation for POST request for /help
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

    watson_context = database.get_watson_context(user_id)

    return {
        "success": True,
        "failure_reason": "None",
        "context": watson_context
    }