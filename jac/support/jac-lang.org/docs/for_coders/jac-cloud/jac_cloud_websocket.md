# websocket

## Walker Declaration
- walker can be declared as websocket thru __specs__ configurations.
- it can still work along with other http methods however, the only limitation is it doesn't support file (maybe in the future).
```python
walker your_event_name {
    has val: int;
    can enter with `root entry {
        report "Do something!";
    }

    class __specs__ {
        has methods: list = ["websocket"];
    }
}
```

## **`Websocket Connection`**
> PROTOCOL: **`ws`** \
> URL: **`/websocket`** \
> HEADER (optional): **`Authorization: Bearer {{USER-TOKEN}}`** \
> QUERY PARAM (optional): **`?channel_id=anystring`**
- once connected, you will recieved first event for connection information
- there's two type of connection
    - Authenticated - with valid Authorization Token
    - Non Authenticated
- you may specify your desired channel_id via query param
    - this will recieved notification from specific channel
    - usage: group chat/notification
```python
{
	"type": "connection",
	"data": {
        # your websocket client id
		"client_id": "1730887348:f46d85203c704c099e9f44e948322a20",

        # user's root_id
		"root_id": "n::672b35cec309e5ef8469c372",

        # non authenticated
		# "root_id": "n::000000000000000000000001",

        # user's channel id, random if not specified
		"channel_id": "1730887348:796ad2e9fa3e484ebe01f071c381b7e8"
	}
}
```

## **`Client Valid Events`**
### Walker
- this will trigger a normal walker as if it was trigger via rest API
```python
{
    # event type
	"type": "walker",

    # walker's name
	"walker": "your_event_name",

    # if you want to recieve a notification for response
	"response": true,

    # walker's request context
	"context": {
        "val": 1
    }
}
```

### User
- this will send notification to target user's clients
- if target user/s has multiple clients, all of it will get notified
```python
{
    # event type
	"type": "user",

    # target user/s via root_id
    "root_ids": ["n::672b35cec309e5ef8469c372"],

    # data you want to send
	"data": {
        "val": 1
    }
}
```

### Channel
- this will send notification to target channel/s
- all clients that's subcribed to the channel will get notified
```python
{
    # event type
	"type": "channel",

    # target channel_id/s
    "channel_ids": ["anystring"],

    # data you want to send
	"data": {
        "val": 1
    }
}
```

### Client
- this will send notification to target client/s
```python
{
    # event type
	"type": "client",

    # target client_ichannel"client_ids": ["1730887348:f46d85203c704c099e9f44e948322a20"],

    # data you want to send
	"data": {
        "val": 1
    }
}
```

### Change User
- migrate from public user to authenticated user and vice versa
```python
{
    # event type
	"type": "change_user",

    # optional - defaults to public user
	"token": "bearer {{user's token}}"
}
```

## **`Walker Client Notification`**
### **`PREREQUISITE`**
```python
import:py from jac_cloud.plugin {WEBSOCKET_MANAGER as socket}
```

### Self
- this will send notification to current websocket it was from (only valid on websocket walker event)
- if via walker api, nothing will happen
```python
socket.notify_self({"any_field": "for_progress", "progress": "0%", "status": "started"});
```

### User
- this will send notification to target user's clients
- if target user/s has multiple clients, all of it will get notified
```python
socket.notify_users([root], {"any_field": "for_progress", "progress": "0%", "status": "started"});
```

### Channel
- this will send notification to target channel/s
- all clients that's subcribed to the channel will get notified
```python
socket.notify_channels([channel_id], {"any_field": "for_progress", "progress": "0%", "status": "started"});
```

### Client
- this will send notification to target client/s
```python
socket.notify_clients([client_id], {"any_field": "for_progress", "progress": "0%", "status": "started"});
```

# **`END TO END INTEGRATION`**
# Jac
```python
"""Websocket scenarios."""
import:py from jac_cloud.plugin {WEBSOCKET_MANAGER as socket}

###########################################################
#                   WEBSOCKET ENDPOINTS                   #
###########################################################

walker send_chat_to_user {
    has root_id: str;

    can enter1 with `root entry {
        _root = &(self.root_id);

        socket.notify_users([_root], {"type": "chat", "data": {"message": "string"}});
    }

    class __specs__ {
        has methods: list = ["websocket", "post"];
    }
}


walker send_chat_to_group {
    has channel_id: str;

    can enter1 with `root entry {
        socket.notify_channels([self.channel_id], {"type": "chat", "data": {"message": "string"}});
    }

    class __specs__ {
        has methods: list = ["websocket", "post"];
    }
}

walker send_chat_to_client {
    has client_id: str;

    can enter1 with `root entry {
        socket.notify_clients([self.client_id], {"type": "chat", "data": {"message": "string"}});
    }

    class __specs__ {
        has methods: list = ["websocket", "post"];
    }
}
```

## **CONNECTION**
**`!!!!!!!!!!!!!!!!!!!!!!!`**\
**`There is no method in the JavaScript WebSockets API for specifying additional headers for the client/browser to send`**\
**`You will need to use 3rd party websocket library that support headers to have authenticated user on connect. Example react-use-websocket & ws`**\
**`Default Javascript Websocket library requires change_user to be authenticated`**
**`!!!!!!!!!!!!!!!!!!!!!!!`**
```js
//####################################################//
//           NOT AUTHENTICATED - JS LIBRARY           //
//####################################################//
const client = new WebSocket("ws://localhost:8000/websocket");

//####################################################//
//             AUTHENTICATED - JS LIBRARY             //
//####################################################//

const client = new WebSocket("ws://localhost:8000/websocket");
client.onopen = (event) => {
  client.send(JSON.stringify({
    "type": "change_user",
    "token": "Bearer {{user's token}}" // optional - default to public user
  }));
};

//####################################################//
//           AUTHENTICATED - NPM WS LIBRARY           //
//####################################################//
import WebSocket from 'ws';

const client = new WebSocket('ws://localhost:8000/websocket', {
  headers: {
    "Authorization": "Bearer {{user's token}}"
  }
});
```
## **CONSUME EVENT**
```js
client.onmessage = (event) => {
  const msg = JSON.parse(event.data);
  switch (msg.type) {
    case "connection":
      // to check connection info
    case "chat":
      console.log(msg.data)
    case "your_event1":
      console.log(msg.data)
    case "your_event2":
      console.log(msg.data)
    case "your_event3":
      console.log(msg.data)
  }
};
```
## **PUBLISH EVENT**
```js
// TRIGGER WALKER EVENT
client.send(JSON.stringify({
	"type": "walker",
	"walker": "your_walker_name",
	"response": true,
	"context": {}
}));

// TRIGGER CLIENT EVENT (ex: direct chat)
client.send(JSON.stringify({
	"type": "client",
	"client_ids": ["target client_id from connection event"],
	"data": {
		"type": "chat",
    "data": {
      "any_field": "any_value"
    }
	}
}));

// TRIGGER CHANNEL EVENT (ex: group chat or chat blast)
client.send(JSON.stringify({
	"type": "channel",
	"channel_ids": ["target channel_id from connection event"],
	"data": {
		  "type": "chat",
      "data": {
        "any_field": "any_value"
      }
	}
}));

// TRIGGER USER EVENT (ex: chat but all target user's client)
client.send(JSON.stringify({
	"type": "user",
	"root_ids": ["target root_id from connection event"],
	"data": {
		"type": "chat",
    "data": {
      "any_field": "any_value"
    }
	}
}));

// TRIGGER CONNECTION EVENT - to get connection info)
client.send(JSON.stringify({
	"type": "connection"
}));
```
---
### **For complete working example you may download this [API Request Collection](https://github.com/amadolid/jaseci/blob/websocket-backup-final/jac-cloud/jac_cloud/tests/jac-cloud-websocket.insomnia)**