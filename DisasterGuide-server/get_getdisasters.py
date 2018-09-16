#!/usr/bin/env python3
"""
Implementation for POST request for /getdisasters
"""

import datetime
from dateutil.relativedelta import relativedelta

def handler(database, severity_threshold):

    response = database.get_severe_disasters(severity_threshold)

    return {
        "success": True,
        "failure_reason": "None",
        "disasters": response
    }