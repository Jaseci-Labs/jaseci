---
title: Socket
---

# **HOW TO SETUP `SOCKET_SVC`**
Socket service is disabled by default. To enable it, you need to update `SOCKET_CONFIG`.
```python
{
    "enabled": True,
    "quiet": False,
    "automated": False,
    "url": os.getenv("SOCKET_URL", "ws://jaseci-socket/ws"),
    "ping_url": os.getenv("SOCKET_PING_URL", "http://jaseci-socket/healthz"),
    "auth": os.getenv("SOCKET_AUTH", "12345678"),
}
```
`automated` is disabled by default. Enabling it will allow JsOrc to regenerate it using `SOCKET_MANIFEST`, similar to *redis*, *elastic* and *prometheus*.

You may run your own websocket. However, you may need to adjust it to cover current Socket service approach.

----

# **`JSSOCKET`**
By default, Socket service uses jssocket as websocket server.

## HOW TO INSTALL
```bash
git clone https://github.com/Jaseci-Labs/jaseci.git
cd jaseci/jaseci_socket
. install.sh
```

## HOW TO SETUP
you may add your preferred authentication by adding environment variable `SOCKET_AUTH`. It must be on the same format as the return from python's `bcrypt.hashpw`. `SOCKET_AUTH` defaults to `1234678` in raw string.
```python
bcrypt.hashpw(
    "your raw password".encode("utf-8"),
    bcrypt.gensalt()
).hex()
```

## HOW TO RUN
```bash
# ----------- default ----------- #
jssocket
# server listening on 0.0.0.0:80
# ------------------------------- #


# -------- preferred port -------- #
jssocket -p 81
jssocket --port 81
# server listening on 0.0.0.0:81
# -------------------------------- #

# -------- preferred host -------- #
jssocket -h localhost
jssocket --host localhost
# server listening on 127.0.0.1:80
# -------------------------------- #

# --- preferred host and port ---- #
jssocket -h localhost --port 81
# server listening on 127.0.0.1:81
# -------------------------------- #
```

## HOW TO USE
#### EVENT STRUCTURE
```js
{
    "type": "YOUR EVENT TYPE",
    "data": { /* your payload */ }
}
```
#### EVENT TYPE
- `server_connect`
    - event used only by jaseci to start up socket service
    - this will authenticate jaseci's socket service. Defaults to 12345678
    - will automatically disconnect when authentication fails
        - OUT EVENT:
            ```js
            {
                "type": "server_connect",
                "data": {
                    "auth": "{{SOCKET_CONFIG'S auth field}}"
                }
            }
            ```
        - IN EVENT:
            ```js
            {
                "type": "server_connect",
                "data": true, // false when authentication fails
            }
            ```
- `client_connect`
    - event used by clients to connect to jssocket
        - OUT EVENT:
            ```js
            {
                "type": "client_connect",
                "data": {
                    "token": "{{current user token}}" // optional
                }
            }
            ```
        - IN EVENT:
            ```js
            {
                "type": "client_connected",
                "data": {
                    "target": "{{current connection id}}"
                    "authenticated": true, // else false for any reason for not being authenticated
                }
            }
            ```
- `client_connected`
    - only server client (jaseci) can send this
    - this is the event triggered by server client (jaseci) in response to client_connect
- `client_disconnect`
    - disconnect to websocket
- `notify_client`
    - notify client with any serializable data
        - OUT EVENT:
            ```js
            {
                "type": "notify_client",
                "data": {
                    "target": "{{other's connection id}}", // optional: default to self connection id
                    "data":  {/* your event data */}
                }
            }
            ```
        - IN EVENT:
            ```js
            {/* your event data */}
            ```
- `notify_group`
    - notify group of clients with any serializable data
    - authenticated user will be included to their master id group
    - non authenticated user will be included to public group
        - OUT EVENT:
            ```js
            {
                "type": "notify_group",
                "data": {
                    "target": "{{other's connection id or group id}}", // optional: default to self connection id
                    // target will check it's current group if connection id is used and this will used as the actual target

                    "data":  {/* your event data */}
                }
            }
            ```
        - IN EVENT:
            ```js
            {/* your event data */}
            ```
- `notify_all`
    - only server client (jaseci) can send this
    - notify all clients with any serializable data
        - OUT EVENT:
            ```js
            {
                "type": "notify_all",
                "data": {/* your event data */}
            }
            ```
        - IN EVENT:
            ```js
            {/* your event data */}
            ```

## SOCKET SERVICE INTEGRATION
### **`NOTIFICATION FROM JAC`**
#### ws.**`notify_client`**
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
> target can be any connnection id \
> else current connection id is used
##### **`HOW TO TRIGGER`**
```js
ws.notify_client(target, {"test": 123456});
```
---
#### ws.**`notify_group`**
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
> target can be any connnection id or user's master id without urn:uuid
> use public if you want to notify all non authenticated user
##### **`HOW TO TRIGGER`**
```js
ws.notify_group(target, {"test": 123456});
```
---
#### ws.**`notify_all`**
> **`Arguments`:** \
> **data**: dict
>
> **`Return`:** \
> None
>
> **`Usage`:** \
> Send notification from jac to all clients
>
##### **`HOW TO TRIGGER`**
```js
ws.notify_all({"test": 123456});
```