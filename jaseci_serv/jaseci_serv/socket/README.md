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
## wb.**`notify`**
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
wb.notify(target, {"test": 123456});
```