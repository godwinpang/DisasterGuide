# JSON specifications

## `POST /adduser HTTP/1.1`

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
    "success": True/False,
    "user_id": <str representing UUID of user>
    "failure_reason": <Description of failure if success is False, else None>
}
```

## `POST /getuser HTTP/1.1`

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

## `POST /addlocation HTTP/1.1`

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

## `POST /getlocation HTTP/1.1`

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

## `POST /getlocationhistory HTTP/1.1`

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

## `GET /getallusers HTTP/1.1`

GET response syntax:
```
{
    "success": True/False
    "failure_reason": <Description of failure if success is False, else None>,
    "data": [
        {
            "first_name": <str representing first name of user>,
            "last_name": <str representing last name of user>,
            "age": <int representing age of user>,
            "role": <str representing role: "first_responder" OR "user">
            "latitude": <float representing latitude>,
            "longitude": <float representing longitude>,
            "status": <bool representing state of user's distress beacon>
            "date_created": date object representing date created
        },
        ...
    ]
}
```

Note that the points returned in the response are given in chronological order from most to least recent.

## `POST /help HTTP/1.1`

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

## `POST /getwatsoncontext HTTP/1.1`

POST request syntax:
```
{
    "user_id": <str representing UUID of user>
    ""
}
```

POST response syntax:
```
{
    "success": True/False
    "failure_reason": <Description of failure if success is False, else None>,
    "context": <dict representing the last recorded Watson context>
}
```

## `POST /adddisaster HTTP/1.1`

POST request syntax:
```
{
    "disaster_id": <str representing UUID of disaster>,
    "disaster_type": <str representing type of natural disaster ("earthquake", "hurricane", etc.)>,
    "latitude": <float representing latitude of approximate center of natural disaster>,
    "longitude": <float representing longitude of approximate center of natural disaster>,
    "radius": <float representing radius of natural disaster>,
    "severity": <float giving approximate severity level, in different scales according to the type>
}
```

POST response syntax:
```
{
    "success": True/False
    "failure_reason": <Description of failure if success is False, else None>
}
```

## `GET /getdisasters HTTP/1.1`

GET response syntax:
```
{
    "success": True/False
    "failure_reason": <Description of failure if success is False, else None>,
    "disasters": [
        {
            "type": <str representing type of natural disaster ("earthquake", "hurricane", etc.)>,
            "center_latitude": <float representing latitude of approximate center of natural disaster>,
            "center_longitude": <float representing longitude of approximate center of natural disaster>,
            "radius": <float representing radius of natural disaster>,
            "severity": <float giving approximate severity level, in different scales according to the type>
        }
        ...
    ]
}
```
