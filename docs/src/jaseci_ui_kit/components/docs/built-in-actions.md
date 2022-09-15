# Update Component 

The update action allows us to update a property of a component.

### Args

0. component property in the format `[component name].[property]`
1. the new value

### Example

"onClick": [
{
"fn": "update",
"args": ["nav.label", "Jaseci 2.0"],
}
]

## Alert

Runs the browser alert function.

### Args

0. alert message

### Example

```JSON
"onClick": [
    {
        "fn": "add",
        "args": [1, 3],
    }
]
```

## Call Endpoint

Runs the browser alert function.

## Properties

- endpoint - the api url that will be called

### Args

0. HTTP Verb
1. Request body

### Example

```JSON
"onClick": [
        {
            "fn": "callEndpoint",
            "endpoint": "http://localhost:3334/message",
            "args": [
                "POST",
                {
                    "message": "Hello!"
                }
            ]
        }
]
```

## Append

Adds a component as a child of another component.

### Args

0. component name
1. component structure - the child component

### Example

```JSON
"onClick": [
    {
        "fn": "append",
        "args": ["msgs",
            {
                "component": "Text",
                "props": {
                    "value": "Hello"
                }
            }
        ],
    }
]

```
