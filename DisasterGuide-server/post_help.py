#!/usr/bin/env python3
"""
Implementation for POST request for /help
"""

def handler(database, event):
    try:
        user_id = event["user_id"]
        description = event["description"]
        watson_context = event["watson_context"]
        distress_status = event["distress_status"] if "distress_status" in event else None
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

    database.log_help_call(user_id, description, watson_context, distress_status)

    return {
        "success": True,
        "failure_reason": "None"
    }