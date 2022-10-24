# **`HOW TO USE SERVICE`**

## `CommonService` (jaseci.svc.common)
This class is the base for implementing service. Dev should use this class if they want to use Service's common attribute and life cycle.

---

## `Common Attributes`

| Attribute | Description |
| ----------- | ----------- |
| app | Attribute for the actual library used in service. For example in TaskService is Celery |
| enabled | If service is enabled in config. The service can be available (upon building) but not enabled (from config) |
| state | For `service life cycle` |
| quiet | For log control and avoid uncessary logs |

---

## `Common Methods`
| Methods | Arguments | Description | Example |
| ----------- | ----------- | ----------- | ----------- |
| `start` | `hook`=nullable | start the actual service based on settings (`kube,config`) | `RedisService().start()` |
| `is_ready` | | check if state is `NOT_STARTED` and app is not yet set | |
| `is_running` | | check if state is `RUNNING` and app is set | |
| `has_failed` | | check if state is `FAILED` | |
| `spawn_daemon` | name_of_daemon=targe_method | spawn daemon threads for background process | `self.spawn_daemon(jsorc=self.interval_check)` |
| `terminate_daemon` | name_of_daemon_to_terminate... | terminate daemon threads | `self.terminate_daemon("jsorc", "other_daemon_name")` |

---

## `Service Life Cycle` (can be overriden)
- `__init__` (initial trigger for `build_service`)
    - this is optional to be overriden if you have additional fields to be use
    - initial state would be `NOT_STARTED`
```python
    def __init__(self, hook=None):
        super().__init__(hook) # run CommonService init
        # ... your other code here ...
```

- `build_kube` (required to be overriden if you have kube settings)
    - will be called upon build and before `build_config`
    - sample kube config are on `jaseci_serv.jaseci_serv.kubes`
```python
    def build_kube(self, hook) -> dict:
        return hook.service_glob("REDIS_KUBE", REDIS_KUBE) # common implementation using global vars
```

- `build_config` (required to be overriden)
    - will be called upon build and after `build_kube`
    - sample config are on `jaseci_serv.jaseci_serv.configs`
```python
    def build_config(self, hook) -> dict:
        return hook.service_glob("REDIS_CONFIG", REDIS_CONFIG) # common implementation using global vars
```

- `run` (required to be overriden)
    - triggered upon `service.start()`
    - upon trigger `start` it still need to check if it's enabled and on ready state (`NOT_STARTED`)
    - if service is not enabled this method will be ignored
    - if service is enabled but state is not equal to `NOT_STARTED` run method will also be ignored
    - if all requirements were met, state will be updated to `STARTED` before running run method
    - if run method raised some exception, state will update to `FAILED` and `failed` method will be called
    - if run method is executed without error state will be updated to `RUNNING`

```python
    def run(self, hook=None):
        self.__convert_config(hook)
        self.app = self.connect() # connect will return Mailer class with stmplib.SMTP (mail.py example)
```

- `post_run` (optional)
    - triggered after `run` method and if state is already set to `RUNNING`

```python
   def post_run(self, hook=None):
        self.spawn_daemon(
            worker=self.app.Worker(quiet=self.quiet).start,
            scheduler=self.app.Beat(socket_timeout=None, quiet=self.quiet).run,
        ) # spawn some threads for Celery worker and scheduler
```

- `failed` (optional)
    - this will be used if you have other process that needs to be executed upon start failure
```python
    def failed(self):
        super().failed()
        self.terminate_daemon("worker", "scheduler") # close some thread when error occurs (task.py example)
```

- `reset` (optional)
    - this will be used if you have other process that needs to be executed upon resetting
```python
    def reset(self, hook):
        if self.is_running():
            self.app.terminate() # app needs to be terminated before calling the actual reset

        super().reset(hook)
```

# `MetaService` (base from `CommonService`)
This class will now be the handler for every service class. It's attributes are different from other services as they are static variable instead of instance variable. This is to have a global handler for every services and will not reinitialize every time it was called.

## `Usage`

- `add_context`
    - for adding a class that used for initalization
```python
        from jaseci.hook import RedisHook
        from jaseci_serv.hook.orm import OrmHook

        ms1 = MetaService()
        ms1.add_context("hook", RedisHook, *args, **kwargs) # args/kwargs are optional

        ms2 = MetaService()
        ms2.get_context("hook")["class"] == RedisHook # True
        ms2.get_context("hook")["args"] == args # True
        ms2.get_context("hook")["kwargs"] == kwargs # True

        ms2.add_context("hook2", RedisHook, *args, **kwargs)
        # is equal to
        MetaService().add_context("hook2", RedisHook, *args, **kwargs)

        ms3 = MetaService()
        ms3.add_context("hook", OrmHook, *args, **kwargs)# will override hook From RedisHook to OrmHook
```

- `get_context`
    - for getting the class without initializing
```python
        from jaseci.hook import RedisHook

        ms1 = MetaService()
        ms1.add_context("hook", RedisHook, *args, **kwargs) # args/kwargs are optional

        ms1.get_context("hook")["class"] == RedisHook # True
        ms1.get_context("hook")["args"] == args # True
        ms1.get_context("hook")["kwargs"] == kwargs # True
```

- `build_context`
    - initialize selected context
```python
        ms1 = MetaService()
        ms1.add_context("hook", RedisHook, *args, **kwargs) # args/kwargs are optional

        hook = ms1.build_context("hook") # hook will be RedisHook instance
```

- `add_service_builder`
    - for adding service class that used for initialization
```python
        ms1 = MetaService()
        ms1.add_service_builder("redis", RedisService)
```

- `build_service`
    - for getting service instance
    - has option to make it disposable or reusable
```python
        ms1 = MetaService()
        backround = False # False == disposable | True == will be reusable and will initialize only once
        redis = ms1.build_service("redis", background, *other_args, **other_kwargs)
```

- `get_service`
    - for getting service instance but it will assume it was on background
    - if it's not yet initialized, it will automatically run `build_service` with `background:True`
```python
        ms1 = MetaService()
        redis = ms1.get_service("redis", *other_args, **other_kwargs)
```

## `Common Builder` (uses `build_context`)
- `build_hook`
    = will call `build_context("hook")` but will run and add some default services such as `kube`, `jsorc`, `promon`, `redis`, `task`, `mail`
```python
        from jaseci.hook import RedisHook
        from jaseci.element.master import Master

        ms1 = MetaService()
        ms1.add_context("hook", RedisHook, *args, **kwargs) # args/kwargs are optional

        hook = ms1.build_hook() # hook will be RedisHook instance
        hook.kube # kube service
        hook.jsorc # jsorc service
        hook.promon # promon service
        hook.redis # redis service
        hook.task # task service
        hook.mail # mail service
        hook.meta # actual meta service
```

- `build_master`
    - will call `build_context("master")` and add `build_context("hook")` for _h
```python
        ###################################################
        #       No need to add this part unless you       #
        #        need to override populate_context        #
        ###################################################
        # from jaseci.hook import RedisHook
        # from jaseci.element.master import Master
        # ms1 = MetaService()
        # ms1.add_context("hook", RedisHook, *args, **kwargs)
        # ms1.add_context("master", Master, *args, **kwargs)
        ###################################################
        #  ---------------------------------------------- #
        ###################################################

        master = ms1.build_master() # hook will be RedisHook instance
        master._h # hook instance
        _h.kube # kube service
        _h.jsorc # jsorc service
        _h.promon # promon service
        _h.redis # redis service
        _h.task # task service
        _h.mail # mail service
        _h.meta # actual meta service
```

- `build_super_master`
    - will call `build_context("super_master")` and add `build_context("hook")` for _h
```python
        ###################################################
        #       No need to add this part unless you       #
        #        need to override populate_context        #
        ###################################################
        # from jaseci.hook import RedisHook
        # from jaseci.element.super_master import SuperMaster
        # ms1 = MetaService()
        # ms1.add_context("hook", RedisHook, *args, **kwargs)
        # ms1.add_context("super_master", SuperMaster, *args, **kwargs)
        ###################################################
        #  ---------------------------------------------- #
        ###################################################

        master = ms1.build_master() # hook will be RedisHook instance
        master._h # hook instance
        _h.kube # kube service
        _h.jsorc # jsorc service
        _h.promon # promon service
        _h.redis # redis service
        _h.task # task service
        _h.mail # mail service
        _h.meta # actual meta service
```

# **`Example Usage`** (StripeService)

```python

import stripe
from jaseci.svc import CommonService
from .config import STRIPE_CONFIG

class StripeService(Co):

    def run(self):
        self.app = stripe
        self.app.api_key = self.config.get("key") # ex: "sk_test_4eC39HqLyjWDarjtT1zdp7dc"

    def build_config(self, hook) -> dict:
        return hook.service_glob("STRIPE_CONFIG", STRIPE_CONFIG)


    def other_method_for_automation1():
        print("run_payment")

    def other_method_for_automation2():
        print("run_add_user")

    def other_method_for_automation3():
        print("run_remove_user")

# ----------------------------------------------- #

from path.to.stripe import StripeService
from jaseci_serv.svc import MetaService

    # ...

    meta = MetaService()
    meta.add_service_build("stripe", StripeService)

    # ...

    # for disposable service
    stripe_service = meta.build_service("stripe", False, hook)
    stripe_service.app.call_any_stripe_methods()

    # for reusable service
    stripe_service1 = meta.get_service("stripe", hook)
    stripe_service2 = meta.get_service("stripe", hook)
    stripe_service3 = meta.get_service("stripe", hook)
    # stripe_service1 == stripe_service2 == stripe_service3

    stripe_service1.app.call_any_stripe_methods()
    stripe_service2.other_method_for_automation2()
    stripe_service3.other_method_for_automation3()