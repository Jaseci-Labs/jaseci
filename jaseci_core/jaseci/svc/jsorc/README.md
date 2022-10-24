# **`HOW TO USE JSORC SERVICE`**

- `JsOrcService` will try to run all of **not** `RUNNING` services but tagged to keep alive
- it will check if it has kube config and will try to add every setting to kubernetes. It will check if it's properly running before it runs the actual service
- if service doesn't have kube config it will just try to rerun the service

## `USAGE`
- adding the service to keep_alive will let the jsorc handle it
- any kube and config for services is set to the actual service not on jsorc

```js

JSORC_CONFIG = {
    "enabled": False,
    "quiet": True,

    // interval checker for each service to keep alive
    "interval": 10,

    // kubernetes namespace
    "namespace": "default",

    // service to keep alive
    "keep_alive": ["promon", "redis", "task", "mail"],
}

```

