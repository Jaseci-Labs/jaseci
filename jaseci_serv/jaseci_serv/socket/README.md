# **HOW TO SETUP `CHANNEL_LAYER`**

## **GLOBAL VARS:** `CHANNEL_LAYER`
### **`IN MEMORY`** *(default)*
```json
{
    "BACKEND": "channels.layers.InMemoryChannelLayer"
}
```
- This config will only works with single jaseci instance. Notification from async walkers will also not work

### **`REDIS`**
```json
{
    "BACKEND": "channels_redis.core.RedisChannelLayer",
    "CONFIG": {
        "hosts": [
            ["localhost", 6379]
        ]
    }
}
```
- This should work on mutiple jaseci instance. Notification from async walker should also work
---
# **`NOTIFICATION FROM JAC`**
## ws.**`notify_channel`**
> **`Arguments`:** \
> **target**: str \
> **data**: dict
>
> **`Return`:** \
> None
>
> **`Usage`:** \
> Send notification from jac to target channel
>
> **`Remarks`:** \
> if user is logged in, `target` can be master id without `urn:uuid:` \
> else used thed `session_id` from client connection
##### **`HOW TO TRIGGER`**
```js
ws.notify_channel(target, {"test": 123456});
```
---
# **`NOTIFICATION FROM JAC`**
## ws.**`notify_group`**
> **`Arguments`:** \
> **target**: str \
> **data**: dict
>
> **`Return`:** \
> None
>
> **`Usage`:** \
> Send notification from jac to target group
>
> **`Remarks`:** \
> if user is logged in, `target` can be master id without `urn:uuid:` \
> else used thed `session_id` from client connection
##### **`HOW TO TRIGGER`**
```js
ws.notify_group(target, {"test": 123456});
```

# **WEB SETUP**
```js
// target can be random string or current token
socket = new WebSocket(`ws://${window.location.host}/ws/socket-server/{{target}}`)
socket.onmessage = (event) => {
    console.log(event);
    // your event handler
    data = JSON.parse(event.data);
    switch(data.type) {
        case "connect":
            // code block
            break;
        case "your-custom-type":
            // code block
            break;
        default:
            // code block
    }
}
// notify backend
socket.send(JSON.stringify({"message": "test"}))
```
## Example connection via `token`
```js
socket = new WebSocket(`ws://${window.location.host}/ws/socket-server/276a40aec1dffc48a25463c3e2545473b45a663364adf3a2f523b903aa254c9f`)
// if token is valid, it's session will be connected to the user's master jid
// all notification from FE will now be send to user's master jid

socket.onmessage = (event) => {
    console.log(event);
}

// all clients that is subscribed to user's master jid will received this notification
socket.send(JSON.stringify({"message": "test"}))
```
#### console.`log`(**event**)
> ![console.log(event)](https://user-images.githubusercontent.com/74129725/267296913-b7b4bdd7-d6c7-49c2-82fe-2d19491daa6c.png "console.log(event)")
#### event.`data`
```txt
{"type": "connect", "authenticated": true, "session_id": null}
```
---
## Example connection **without** `token`
```js
socket = new WebSocket(`ws://${window.location.host}/ws/socket-server/any-ranmdom-string`)
// this socket will be subscribed to a random uuid
// you will need to use that random uuid on wb.notify as target params
// FE is required to send it on walkers with wb.notify to override target

socket.onmessage = (event) => {
    console.log(event);
    // you may get session_id from JSON.parse(event.data).session_id
}

// not advisable but still can be used for notifying that random uuid
socket.send(JSON.stringify({"message": "test"}))
```
#### console.`log`(**event**)
> ![console.log(event)](https://user-images.githubusercontent.com/74129725/267294795-032a7d78-0124-4db5-bed7-5858e7d72774.png "console.log(event)")
#### event.`data`
```txt
{"type": "connect", "authenticated": false, "session_id": "53a0e05e-8689-4e87-984d-dbd4bad58c9d"}
```