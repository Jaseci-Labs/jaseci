# Creating an API Endpoint

The webkit is able to call api endpoints, as long as the api endpoint sends back a list of supported / built-in actions.

For example, let's say we want to alert a message on the frontend. To do so, we'll need to ensure that the response body for the api endpoint is an array that contains an alert action.

#### Example API Endpoint

```JS
Route.post('/alert-message', async ({ request }) => {
  return [
    {
      fn: 'alert',
      args: [`Hey, how are you?`],
    },
    {
      fn: 'alert',
      args: [`How is the weather?`],
    },
  ]
})
```

From the code above, once it reaches the frontend, each action specified in the array will execute; you should see two alert messages.

## Calling the Endpoint

Once the api endpoint is ready, we can call it on the frontend with the `callEndpoint` action.

For example:

```JSON
{
    "component": "Button",
    "props": {
        "label": "Alert Messages"
    },
    "events": {
        "onClick": [
            {
                "fn": "callEndpoint",
                "endpoint": "http://localhost:3334/alert-message",
                "args": [
                    "POST",
                    {}
                ]
            }
        ]
    }
}

```

The callEndpoint action can receive optional args, the HTTP verb and the request body.