# JSON specifications

## POST /adduser

POST request syntax:
```
{
    "user_id": <str representing UUID of user; optional>,
    "first_name": <str representing first name>,
    "last_name": <str representing last name>,
    "birthday": {
        "month": <int representing month, indexed from 1>,
        "day": <int representing day>,
        "year": <int representing year>
    },
    "role": <"first_responder" OR "user">
}
```

POST response syntax:
```
{
    "success": True/False
    "failure_reason": <Description of failure if success is False, else None>,
}
```

## POST /getuser

POST request syntax:
```
{
    "user_id": <str representing UUID of user>
}
```

POST response syntax:
```
{
    "success": True/False
    "failure_reason": <Description of failure if success is False, else None>,
    "first_name": <str representing first name>
    "last_name": <str representing last name>
    "age": <int representing age>
    "role": <"first_responder" OR "user">,
    "distress_status" <True OR False>
}
```

## POST /addlocation

POST request syntax:
```
{
    "user_id": <str representing UUID of user>,
    "latitude": <float representing latitudinal coordinate>,
    "longitude": <float representing longitudinal coordinate>
}
```

POST response syntax:
```
{
    "success": True/False
    "failure_reason": <Description of failure if success is False, else None>
}
```

## POST /getlocation

POST request syntax:
```
{
    "user_id": <str representing UUID of user>
}
```

POST response syntax:
```
{
    "success": True/False
    "failure_reason": <Description of failure if success is False, else None>,
    "latitude": <float representing latitude>,
    "longitude": <float representing longitude>,
    "date_created": <datetime object representing date and time location was logged>
}
```

## POST /getlocationhistory

POST request syntax:
```
{
    "user_id": <str representing UUID of user>
}
```

POST response syntax:
```
{
    "success": True/False
    "failure_reason": <Description of failure if success is False, else None>,
    "locations": [
        {
            "latitude": <float representing latitude>,
            "longitude": <float representing longitude>,
            "date_created": date object representing date created
        },
        ...
    ]
}
```

## GET /getallusers

GET response syntax:
```
{
    "success": True/False
    "failure_reason": <Description of failure if success is False, else None>,
    "locations": [
        {
            "latitude": <float representing latitude>,
            "longitude": <float representing longitude>,
            "date_created": date object representing date created
        },
        ...
    ]
}
```

Note that the points returned in the response are given in chronological order from most to least recent.

## POST /help

POST request syntax:
```
{
    "user_id": <str representing UUID of user>,
    "description": <str representing description of user's input in text>,
    "watson_context": <dict structure representing Watson's context>,
    "distress_status": <bool representing distress beacon status>
    ""
}
```

POST response syntax:
```
{
    "success": True/False
    "failure_reason": <Description of failure if success is False, else None>
}
```