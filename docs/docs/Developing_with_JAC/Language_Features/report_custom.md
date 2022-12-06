# **Report Custom**
Supports custom structure as response body.

## **Syntax**
```js
    report:custom = `{{ any | {} | [] }}`
```

## **Usage**
This can be combine with walker_callback as 3rd party service requires different json structure on response.
It can also be used for different scenario that doesn't require ctx structure