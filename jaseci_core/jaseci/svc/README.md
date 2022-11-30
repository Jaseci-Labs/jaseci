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
## `Service Settings`
### `Config`
- service use MemoryHook's service_glob method. This will automatically add default config if it's not existing
- You need to use ConfigApi (config_set and config_refresh) to update configs on every hooks including redis.
- If config is updated through admin portal and redis is running, redis needs to remove the old copy of config since redis is the first hook where the service get the configs
    ```json
    // Structure
    {
        "enabled": True,
        "quiet": True,
        "field1": "val1",
        "field1": "val2",
        "field1": "val3",
        ...
    }

    ```
### `Kube`
- this is similart to config's behavior but it uses different structure

    ```json
        // Structure: grouped values from `yaml.safe_load_all(...yaml_file...)`
        // map each safe_load_all to $.kind
        {
            "ServiceAccount": [
                {
                    "apiVersion": "v1",
                    "kind": "ServiceAccount",
                    "metadata": {
                        "labels": {
                            "helm.sh/chart": "kube-state-metrics-4.13.0",
                            "app.kubernetes.io/managed-by": "Helm",
                            "app.kubernetes.io/component": "metrics",
                            "app.kubernetes.io/part-of": "kube-state-metrics",
                            "app.kubernetes.io/name": "kube-state-metrics",
                            "app.kubernetes.io/instance": "jaseci-prometheus",
                            "app.kubernetes.io/version": "2.5.0",
                        },
                        "name": "jaseci-prometheus-kube-state-metrics",
                        "namespace": "default",
                    },
                    "imagePullSecrets": [],
                }
            ]
        }
    ```

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

- `build_manifest` (required to be overriden if you have kube settings)
    - will be called upon build and before `build_config`
    - sample kube config are on `jaseci.svc.redis.manifest`
```python
    def build_manifest(self, hook) -> dict:
        return hook.service_glob("REDIS_MANIFEST", REDIS_MANIFEST) # common implementation using global vars
```

- `build_config` (required to be overriden)
    - will be called upon build and after `build_manifest`
    - sample config are on `jaseci.svc.config`
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
    def reset(self, hook, start):
        if self.is_running():
            self.app.terminate() # app needs to be terminated before calling the actual reset

        super().reset(hook)
```
---
# `MetaService` (base from `CommonService`)
This class will now be the handler for every service class with the help of `JsOrc`. MetaService's attributes are different from other services as they are static variable instead of instance variable. This is to have a global handler for every services and will not reinitialize every time it was called. This Service can't be disabled and will always shows logs.

`JsOrc` will be the app that MetaService will use to hold every context and services. It also holds the initalization part of that values.

## `CONFIG`

```python
KUBERNETES_CONFIG = {"in_cluster": True, "config": None}

META_CONFIG = {
    # if jsorc will have the power to re/build itself
    "automation": False,

    # waiting time before the next interval is triggered
    "backoff_interval": 10,

    # jsorc namespace. Initially for cluster but should be used on every other settings
    "namespace": "default",

    # name of services that needs to be check for every interval
    "keep_alive": ["promon", "redis", "task", "mail"],

    # this config use for kubectl configs
    "kubernetes": KUBERNETES_CONFIG,
}
```

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

class StripeService(CommonService):

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

```

---
# **`Automation `**(`JsOrc`)
This will only happen if META_CONFIG is set to be automated.
- `JsOrc` will try to run all **not** `RUNNING` services but tagged to keep alive
- it will check each service if it has kube config and will try to add every setting to cluster.
- It will also check in the cluster if the pod state is running before it tries to re/run the actual service
- if service doesn't have kube config it will just try to rerun the service

## `!!!PREREQUISITE!!!`
- `config_set` trigger
```js
{
	"name": "META_CONFIG",
	"value": {
		"automation": true,
		"backoff_interval": 10,
		"namespace": "default",
		"keep_alive": [
			"promon",
			"redis",
			"task",
			"mail"
		],
		"kubernetes": {
			"in_cluster": true,
			"config": null
		}
	},
	"do_check": false
}
```
- `service_refresh` trigger
```js
{
    "name": "meta"
}
```
- `JsOrc` should do it's thing


## `USAGE`
- adding the service to keep_alive will let the jsorc handle it
- any `{{NAME}}_MANIFEST` and `{{NAME}}_CONFIG` is set to the actual service not on `JsOrc`

## `EXAMPLE`

### `with` kube config
- [prometheus.py](../prometheus/prometheus.py)
- [kube.py](../prometheus/kube.py)
    - `PROMON_MANIFEST` == grouped values from `yaml.safe_load_all(...yaml_file...)`
        - ex:
        ```json
            // map each safe_load_all to $.kind
            {
                "ServiceAccount": [
                    {
                        "apiVersion": "v1",
                        "kind": "ServiceAccount",
                        "metadata": {
                            "labels": {
                                "helm.sh/chart": "kube-state-metrics-4.13.0",
                                "app.kubernetes.io/managed-by": "Helm",
                                "app.kubernetes.io/component": "metrics",
                                "app.kubernetes.io/part-of": "kube-state-metrics",
                                "app.kubernetes.io/name": "kube-state-metrics",
                                "app.kubernetes.io/instance": "jaseci-prometheus",
                                "app.kubernetes.io/version": "2.5.0",
                            },
                            "name": "jaseci-prometheus-kube-state-metrics",
                            "namespace": "default",
                        },
                        "imagePullSecrets": [],
                    }
                ]
            }
        ```

```python
# ... other imports
from .manifest import PROMON_MANIFEST
class PromotheusService(CommonService):
    # ... all other codes ...
    def build_manifest(self, hook) -> dict:
        return hook.service_glob("PROMON_MANIFEST", PROMON_MANIFEST)
```
- since `promon` is included on keep_alive, `JsOrc` will include it on `interval_check`
- during `interval_check`, `JsOrc` will try to add every kube configuration from `PROMON_MANIFEST` grouped by commands
- on first `interval_check`, it is expected to ignore the rerun of the `promon` service because the pods that has been generated is **`not`** yet fully initialized and running.
- subsequent `interval_check` should have the ability to restart the `promon` service since pods for prometheus server should be available by that time (this may vary depends on network or server)
- if `promon` is now running it will now be ignored on next `interval_check`

### `without` kube config
- [task.py](../task/task.py)
- if it's not yet running, every `interval_check` will check if TaskService is running.
- if it returns false, it will just run task.reset(hook)

## `SUMMARY`
- Initialization of every service included in `keep_alive` config should be automatically handled by `JsOrc`.

---

# `Configuration API's`

## `config_set`
 - for updating service configs
 - ex: `MetaService`
    > ```js
    > {
    >     "name": "META_CONFIG",
    >     "value": {
    >         "automation": true,
    >         "backoff_interval": 10,
    >         "namespace": "default",
    >         "keep_alive": [
    >             "promon",
    >             "redis",
    >             "task",
    >             "mail"
    >         ],
    >         "kubernetes": {
    >             "in_cluster": true,
    >             "config": null
    >         }
    >     },
    >     "do_check": false
    > }
    > ```


## `apply_yaml` (to be renamed)
 - for updating service's kubernetes manifest
 - uses multipart/form-data since it needs the yaml file
 - this will also have mechanism for automatic versioning to be able to use the patching features in cluster
 - this can handle create/patch/delete mechanism
 - currently, not all kind of manifest have permission to be deleted. For ex: `PersistentVolumeClaim`, to delete this kind of manifest you need to specify `unsafe_paraphrase` field with value of `I know what I'm doing!` case sensitive. This is to verify that you really know what you're doing.
 - ex: `PROMON_MANIFEST`
    > ```js
    > const form = new FormData();
    > form.append('name', 'PROMON_MANIFEST');
    > form.append('file', File(['<data goes here>'], '...\\prometheus.yaml'));
    > // not needed if for safe patching/deleting only
    > form.append('unsafe_paraphrase', 'I know what I\'m doing!')
    >
    > fetch('.../apply_yaml', {
    >   method: 'POST',
    >   headers: {...},
    >   body: form
    > });
    > ```

## `service_refresh`
 - for restarting service
 - if automation is enabled. This will just resync the configs and let `JsOrc` handle the rest
 - ex: `MetaService`
    > ```js
    > {
    >   // name of service in hook [task/redis/promon/mail/meta]
    >   "name": "meta"
    > }
    > ```
