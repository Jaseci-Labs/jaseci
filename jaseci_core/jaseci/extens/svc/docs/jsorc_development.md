# JsOrc Development

#### **SETTINGS** ([JsOrcSettings](../../../jaseci_core/jaseci/jsorc_settings.py))
- this will holds default configuration for services and it's manifest

#### **CONFIG** ([JsOrcSettings](../../../jaseci_core/jaseci/jsorc_settings.py).`JSORC_CONFIG`)
```python
# JsOrc is always enabled
{
    # this will be the interval for regeneration
    "backoff_interval": 10,

    # preloaded services is included on initial JsOrc regenerate
    "pre_loaded_services": ["kube", "redis", "prome", "mail", "task", "elastic"],
}
```

#### **REGENERATION**
- JsOrc are now always enabled and will try to regenerate.
    - Initial regen sequence
        - trigger after build up
        - will check for db connection (if enabled in [JsOrcSettings](../../../jaseci_core/jaseci/jsorc_settings.py).`DB_REGEN_CONFIG`)
            - connected: skip the spawing of `jaseci-db`
            - not connected: will try to spawn `jaseci-db` using [JsOrcSettings](../../../jaseci_core/jaseci/jsorc_settings.py).`DB_REGEN_MANIFEST`
            - recheck again if it can establish the connection (loop until connection is established)
                - once connected: `raise SystemExit`
                - this is to restart the pod and be able to process makemigrations/migrate
        - jaseci should now have a proper db connection
        - JsOrc will now try to load every pre_loaded_services
            - if failure occured on service initialization
                - try to apply manifest and spawn the needed pods
                - retry to initialize
                    - failed: tagged it again for regeneration
        - JsOrc should now have all pre_loaded_services loaded
    - Interval regen
        - every `{{backoff_interval}}` seconds
        - it will ignore additional trigger if previous regeneration is still happening



---

# **`Pillars`**

## **`Service`**
#### **Features**
- Lazy Loading
    - it will only initialized when needed unless it was tagged as automated in config
- Automation
    - if enabled: it will be included on the regeneration process once error occured

#### **Prerequisite**
    - class should be decorated as service and extend from JsOrc.CommonService

#### **Syntax**
- **`Declaration`**
```python
from jaseci import JsOrc

@JsOrc.service(
    # name of the service
    name="redis",

    # service config
    config="REDIS_CONFIG",

    # nullable
    # used for regeneration and spawning kube
    # from JsOrcSettings as default then db/redis later on
    manifest="REDIS_MANIFEST",

    # when you have multiple version of the class and have the same name
    # highest value will be used
    priority=0, # defaults to zero

    # allow to use proxy (Fake not running service) when trying to build a hook
    # this is to avoid error on startup since django are not yet fully initialized
    proxy=True,
)
class RedisService(JsOrc.CommonService):
    # your implementation
```
- **`Accessing`**
```python
from jaseci import JsOrc

def any_method():
    redis = JsOrc.svc("redis")
```

#### **Common Attributes**

| Attribute | Description |
| ----------- | ----------- |
| app | Attribute for the actual library used in service. For example in TaskService is Celery |
| enabled | If service is enabled in config. The service can be available (upon building) but not enabled (from config) |
| automated | If service is automated in config. The service will be part of regeneration if it can't initialized properly |
| state | For `service life cycle` |
| quiet | For log control and avoid uncessary logs |

#### **Common Methods**
| Methods | Arguments | Description | Example |
| ----------- | ----------- | ----------- | ----------- |
| `poke` | `cast`= nullable, `msg` = nullable | poke will try to check if the service is running. Throw the error `msg` (else default mesesage) if not running. `cast` is for casting the returned value of poke. if casted to the current service class, it will return the service instance instead of the service.app | `JsOrc.svc("redis").poke()` |
| `is_ready` | | check if state is `NOT_STARTED` and app is not yet set | |
| `is_running` | | check if state is `RUNNING` and app is set | |
| `has_failed` | | check if state is `FAILED` | |
| `spawn_daemon` | name_of_daemon=targe_method | spawn daemon threads for background process | `self.spawn_daemon(jsorc=self.interval_check)` |
| `terminate_daemon` | name_of_daemon_to_terminate... | terminate daemon threads | `self.terminate_daemon("jsorc", "other_daemon_name")` |

#### **Service Life Cycle** (can be overriden)
- **\_\_init\_\_** ()
    - this is optional to be overriden if you have additional fields to be use
    - initial state would be `NOT_STARTED`
```python
    def __init__(self, config: dict, manifest: dict):
        super().__init__(config, manifest) # run CommonService init
        # ... your other code here ...
```

- **run** (required to be overriden)
    - triggered upon `service.start()`
    - upon trigger `start` it still need to check if it's enabled and on ready state (`NOT_STARTED`)
    - if service is not enabled this method will be ignored
    - if service is enabled but state is not equal to `NOT_STARTED` run method will also be ignored
    - if all requirements were met, state will be updated to `STARTED` before running run method
    - if run method raised some exception, state will update to `FAILED` and `failed` method will be called
    - if run method is executed without error state will be updated to `RUNNING`

```python
    # redis_svc.py
    def run(self):
        self.app = Redis(**self.config, decode_responses=True)
        self.app.ping()
```

- **post_run** (optional)
    - triggered after `run` method and if state is already set to `RUNNING`

```python
    # task_svc.py
    def post_run(self):
        self.spawn_daemon(
            worker=self.app.Worker(quiet=self.quiet).start,
            scheduler=self.app.Beat(socket_timeout=None, quiet=self.quiet).run,
        ) # spawn some threads for Celery worker and scheduler
```

- **failed** (optional)
    - this will be used if you have other process that needs to be executed upon start failure
```python
    # task_svc.py
    def failed(self):
        super().failed()
        self.terminate_daemon("worker", "scheduler") # close some thread when error occurs (task.py example)
```

- **on_delete** (optional)
    - this will be used if you have other process that needs to be executed upon resetting
```python
    # task_svc.py
    def on_delete(self): # will be trigger once garbage collected
        self.terminate_daemon("worker", "scheduler")
```

---
## **`Repository`**
#### **Features**
- targetted class should be related on any datasource such as database, redis and etc
- to handle class overriding even on lower build
> ex: jaseci_serv's orm_hook
>
> If you want to initialize hook on jaseci_core you may only use RedisHook/MemoryHook class.
> If you try to run it with jaseci_serv, you may still need to cast it to OrmHook before you may be able to use it.
> JsOrc will try to handle it for you. If you try to get repository class, it will try to get the highest priority class even the source code doesn't have access on it.
> Let say you have `MemoryHook` [prio 0] / `RedisHook` [prio 1] / `OrmHook` [prio 2] classes and tagged as `hook`. `JsOrc.src("hook") or JsOrc.hook()` will always return `OrmHook` even you initialized it on jaseci_core as long as `OrmHook` class is loaded

#### **Syntax**
- **`Declaration`**
```python
from jaseci import JsOrc

@JsOrc.repository(
    name="hook",
    priority=0
)
class MemoryHook():
    # your implementation

@JsOrc.repository(
    name="hook",
    priority=1
)
class RedisHook():
    # your implementation

@JsOrc.repository(
    name="hook",
    priority=2
)
class OrmHook():
    # your implementation
```
- **`Accessing`**
```python
from jaseci import JsOrc

def anywhere_any_method():
    hook = JsOrc.src("hook") # or JsOrc.hook()
    hook # == OrmHook instance as long as it's class is loaded
```

## **`Context`**

#### **Features**
- no restriction on class but similar to repository

#### **Syntax**
- **`Declaration`**
```python
from jaseci import JsOrc

@JsOrc.context(
    name="master",
    priority=0
)
class Master():
    # your implementation

@JsOrc.context(
    name="master",
    priority=1
)
class Master2():
    # your implementation

@JsOrc.context(
    name="master",
    priority=2
)
class Master3():
    # your implementation
```
- **`Accessing`**
```python
from jaseci import JsOrc

def anywhere_any_method():
    master1 = JsOrc.ctx("master") # always new instance
    master1 # == Master3 instance as long as it's class is loaded

    master2 = JsOrc.get("master") # will use persisting instance
    master1 != master2 # True
    master2 == JsOrc.get("master") # True
    JsOrc.destroy("master") # destroy persisting instance
    JsOrc.renew("master") # destroy if existing then create another persisting instance
```

# **`Additional Feature`** (preferably for testing)

```python
from jaseci import JsOrc

@JsOrc.inject(
    services = [
        "mail", # mail service
        ("task", "task_alias") # task service with alias
    ],
    repositories = [
        "hook", # OrmHook and always new instance
        ("hook", "any_alias") # OrmHook but with alias
    ],
    context = [
        "master", # always new instance
    ]
)
def anywhere_any_method(mail, task_alias, hook, any_alias, master):
    # your testing or implementation
```