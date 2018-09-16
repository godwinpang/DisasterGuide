#!/usr/bin/env python3
"""
Implementation for POST request for /getallusers
"""

import datetime
from dateutil.relativedelta import relativedelta

def handler(database):

    users = database.get_all_users()

    return {
        "success": True,
        "failure_reason": "None",
        "data": [
            {
                "first_name": u[1],
                "last_name": u[2],
                "age": relativedelta(datetime.datetime.now().date(), u[3]).years,
                "latitude": u[4],
                "longitude": u[5],
                "status": database.get_distress_status(u[0])
            } for u in users if u[0] != database.NULL_UUID
        ]
    }