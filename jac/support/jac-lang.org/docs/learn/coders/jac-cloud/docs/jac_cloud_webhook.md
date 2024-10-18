# WEBHOOK
- webhook walker is similar to normal authenticated walker however, normal authenticated walker is associated to a user while webhook is directly to root.
- webhook api keys are manage by user
- supports different HTTP components as API key holder
  - header (default):
  - query
  - path
  - body
- name of the api-key can be change to any string (default: `X-API-KEY`)

## CREATE WEBHOOK
```python
walker webhook {
    can enter1 with `root entry {
        report here;
    }

    class __specs__ {
        has webhook: dict = {
            "type": "header | query | path | body", # optional: defaults to header
            "name": "any string" # optional: defaults to X-API-KEY
        };
    }
}
```
![image](https://github.com/user-attachments/assets/75cceb2d-5618-4f68-97e2-31a4270e70b1)

# WEBHOOK MANAGEMENT APIs
![image](https://github.com/user-attachments/assets/3a01ab35-06b0-4942-8f1f-0c4ae794ce21)

## GENERATE API KEY
#### `REQUEST`
> **POST** /webhook/generate-key
```python
{
  # unique name of webhook
  "name": "webhook1",

  # names of allowed webhook walkers. Not set or empty list means all webhook walkers is allowed.
  "walkers": ["webhook"],

  # names of allowed nodes. Not set or empty list means all nodes is allowed.
  "nodes": ["root"],

  # date now + timedelta( {{interval}}: {{count}} )
  "expiration": {
    "count": 60,

    # seconds | minutes | hours | days
    "interval": "days"
  }
}
```
#### `RESPONSE`
```python
{
  "id": "672203ee093fd3d208a4b6d4",
  "name": "webhook1",
  "key": "6721f000ee301e1d54c3de3d:1730282478:P4Nrs3DOLIkaw5aYsbIWNzWZZAwEyb20"
}
```

## GET API KEY
#### `REQUEST`
> **GET** /webhook
#### `RESPONSE`
```python
{
  "keys": [
    {
      "id": "672203ee093fd3d208a4b6d4",
      "name": "test",
      "root_id": "6721f000ee301e1d54c3de3d",
      "walkers": ["webhook"],
      "nodes": ["root"],
      "expiration": "2025-12-24T10:01:18.206000",
      "key": "6721f000ee301e1d54c3de3d:1730282478:P4Nrs3DOLIkaw5aYsbIWNzWZZAwEyb20"
    }
  ]
}
```

## EXTEND API KEY
#### `REQUEST`
> **PATCH** /webhook/extend/`{id}`
```python
{
  "count": 60,

  # seconds | minutes | hours | days
  "interval": "days"
}
```
#### `RESPONSE`
```python
{
  "message": "Successfully Extended!"
}
```

## DELETE API KEY
#### `REQUEST`
> **DELETE** /webhook/delete
```python
{
  # list of id to be deleted
  "ids": ["672203ee093fd3d208a4b6d4"]
}
```
#### `RESPONSE`
```python
{
  "message": "Successfully Deleted!"
}
```
