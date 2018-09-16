# JSON specifications

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
    "location": [float representing latitude, float representing longitude],
    "date_created": <datetime object representing date and time location was logged>
}
```

## POST /getalllocations

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

Note that the points returned in the response are given in chronological order from most to least recent.

## POST /adduser

POST request syntax:
```
{
    "user_id": <str representing UUID of user>,
    "first_name": <str representing first name>,
    "last_name": <str representing last name>,
    "birthday": {
        "month": <int representing month, indexed from 1>,
        "day": <int representing day>,
        "year": <int representing year>
    }
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

