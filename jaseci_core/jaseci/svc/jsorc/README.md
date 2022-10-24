# **`HOW TO USE JSORC SERVICE`**

- `JsOrcService` will try to run all of **not** `RUNNING` services but tagged to keep alive
- it will check each service if it has kube config and will try to add every setting to kubernetes.
- It will also check on the cluster if the service is properly running before it runs the actual jaseci service
- if service doesn't have kube config it will just try to rerun the service

## **`!! PREREQUISITE !!`**
- Kubernetes should be `enabled`, `running` and `connected`
- JsOrc should be `enabled` and `running`

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

## `EXAMPLE`

### `with` kube config
- [prometheus.py](../prometheus/prometheus.py)
- [kube.py](../prometheus/kube.py)
        - `PROMON_KUBE` == `yaml.safe_load(...yaml_file...)`

```python
# ... other imports

from .kube import PROMON_KUBE

class PromotheusService(CommonService):

    # ... all other codes ...

    def build_kube(self, hook) -> dict:
        return hook.service_glob("PROMON_KUBE", PROMON_KUBE)

```
- since `promon` is included on keep_alive, JsOrcService will include it on `interval_check`
- during `interval_check`, JsOrcService will try to add every kube configuration from `PROMON_KUBE` grouped by commands
- on first `interval_check`, it is expected to ignore the rerun of the `promon` service because the pods that has been generated is **`not`** yet fully initialized and running.
- subsequent `interval_check` should have the ability to restart the `promon` service since pods for prometheus server should be available by that time (this may vary depends on network or server)
- if `promon` is now running it will now be ignored on next `interval_check`

### `without` kube config
- [task.py](../task/task.py)
- if it's not yet running, every `interval_check` will check if TaskService is running.
- if it returns false, it will just run task.reset(hook)


## `SUMMARY`
- Initialization of every service included in `keep_alive` config should be automatically handled by jsorc. JsOrc restarting a service is identical to triggering it via `config_refresh` api