# Jac API Collections


## APIs for actions

This set action APIs enable the manual management of Jaseci actions and action libraries/sets. Action libraries can be loaded locally into the running instance of the python program, or as a remote container linked action library. In this mode, action libraries operate as micro-services. Jaseci will be able to dynamically and automatically make this decision for the user based on online monitoring and performance profiling.

### Actions Load Local
```
cli: actions load local | api: actions_load_local | auth: admin
file: str (*req)
```
This API will dynamically load a module based on a python file. The module is loaded directly into the running Jaseci python instance. This API also makes an attempt to auto detect and hot load any python package dependencies the file may reference via python's relative imports. This file is assumed to have the necessary annotations and decorations required by Jaseci to recognize its actions.
#### Params
Params file -- The python file with full to load actions from. (i.e., ~/local/myact.py)

### Actions Load Remote
```
cli: actions load remote | api: actions_load_remote | auth: admin
url: str (*req)
```
This API will dynamically load a set of actions that are present on a remote server/micro-service. This server must be configured to interact with Jaseci properly. This is easily achieved using the same decorators used for local action libraries. Remote actions allow for higher flexibility in the languages supported for action libraries. If an library writer would like to use another language, the main hook REST api simply needs to be implemented. Please refer to documentation on creating action libraries for more details.
#### Params
Params url -- The url of the API server supporting Jaseci actions.

### Actions Load Module
```
cli: actions load module | api: actions_load_module | auth: admin
mod: str (*req)
```
This API will dynamically load a module using python's module import format. This is particularly useful for pip installed action libraries as the developer can directly reference the module using the same format as a regular python import. As with load local, the module will be loaded directly into the running Jaseci python instance.
#### Params
Params mod -- The import style module to load actions from. (i.e., jaseci_ai_kit.bi_enc)

### Actions List
```
cli: actions list | api: actions_list | auth: admin
name: str ()
```
This API is used to list the loaded actions active in Jaseci. These actions include all types of loaded actions whether it be local modules or remote containers. A particular set of actions can be viewed using the name parameter.

#### Params
Params name -- The name for a library for which to filter the view of shown actions. If left blank all actions from all loaded sets will be shown.

### Actions Module List
```
cli: actions module list | api: actions_module_list | auth: admin
detailed: bool (False)
No documentation yet.
```

### Actions Unload Module
```
cli: actions unload module | api: actions_unload_module | auth: admin
name: str (*req)
No documentation yet.
```

### Actions Unload Action
```
cli: actions unload action | api: actions_unload_action | auth: admin
name: str (*req)
No documentation yet.
```

### Actions Unload Actionset
```
cli: actions unload actionset | api: actions_unload_actionset | auth: admin
name: str (*req)
No documentation yet.
```

## APIs for architype

The architype set of APIs allow for the addition and removing of architypes. Given a Jac implementation of an architype these APIs are designed for creating, compiling, and managing architypes that can be used by Jaseci. There are two ways to add an architype to Jaseci, either through the management of sentinels using the sentinel API, or by registering independent architypes with these architype APIs. These APIs are also used for inspecting and managing existing arichtypes that a Jaseci instance is aware of.

### Architype Register
```
cli: architype register | api: architype_register | auth: user
code: str (*req), encoded: bool (False), snt: Sentinel (None)
```

This register API allows for the creation or replacement/update of an architype that can then be used by walkers in their interactions of graphs. The code argument takes Jac source code for the single architype. To load multiple architypes and walkers at the same time, use sentinel register API.

#### Params
Params code -- The text (or filename) for an architypes Jac code
encoded -- True/False flag as to whether code is encode in base64
snt -- The UUID of the sentinel to be the owner of this architype

#### Returns
Returns - Fields include 'architype': Architype object if created otherwise null 'success': True/False whether register was successful 'errors': List of errors if register failed 'response': Message on outcome of register call

### Architype Get
```
cli: architype get | api: architype_get | auth: user
arch: Architype (*req), mode: str (default), detailed: bool (False)
No documentation yet.
```

#### Params
Params arch -- The architype being accessed
mode -- Valid modes: {default, code, ir, }
detailed -- Flag to give summary or complete set of fields

#### Returns
Returns - Fields include (depends on mode) 'code': Formal source code for architype 'ir': Intermediate representation of architype 'architype': Architype object print

### Architype Set
```
cli: architype set | api: architype_set | auth: user
arch: Architype (*req), code: str (*req), mode: str (default)
No documentation yet.
```

#### Params
Params arch -- The architype being set
code -- The text (or filename) for an architypes Jac code/ir
mode -- Valid modes: {default, code, ir, }

#### Returns
Returns - Fields include (depends on mode) 'success': True/False whether set was successful 'errors': List of errors if set failed 'response': Message on outcome of set call

### Architype List
```
cli: architype list | api: architype_list | auth: user
snt: Sentinel (None), kind: str (None), detailed: bool (False)
No documentation yet.
```

#### Params
Params snt -- The sentinel for which to list its architypes
detailed -- Flag to give summary or complete set of fields
kind -- Architype kind used to narrow the result set

#### Returns
Returns - List of architype objects

### Architype Count
```
cli: architype count | api: architype_count | auth: user
snt: Sentinel (None), kind: str (None)
No documentation yet.
```

#### Params
Params snt -- The sentinel for which to list its architypes
detailed -- Flag to give summary or complete set of fields
kind -- Architype kind used to narrow the result set from which the count is evaluated

#### Returns
Returns - Count of architype objects

### Architype Delete
```
cli: architype delete | api: architype_delete | auth: user
arch: Architype (*req), snt: Sentinel (None)
No documentation yet.
```

#### Params
Params arch -- The architype being set
snt -- The sentinel for which to list its architypes

#### Returns
Returns - Fields include (depends on mode) 'success': True/False whether command was successful 'response': Message on outcome of command

## APIs for config

Abstracted since there are no valid configs in core atm, see jaseci_serv to see how used.

### Config Get
```
cli: config get | api: config_get | auth: admin
name: str (*req), do_check: bool (True)
No documentation yet.
```

### Config Set
```
cli: config set | api: config_set | auth: admin
name: str (*req), value: str (*req), do_check: bool (True)
No documentation yet.
```

### Config List
```
cli: config list | api: config_list | auth: admin
n/a
No documentation yet.
```

### Config Index
```
cli: config index | api: config_index | auth: admin
n/a
No documentation yet.
```

### Config Exists
```
cli: config exists | api: config_exists | auth: admin
name: str (*req)
No documentation yet.
```

### Config Delete
```
cli: config delete | api: config_delete | auth: admin
name: str (*req), do_check: bool (True)
No documentation yet.
```

## APIs for global

No documentation yet.

### Global Set
```
cli: global set | api: global_set | auth: admin
name: str (*req), value: str (*req)
No documentation yet.
```

### Global Delete
```
cli: global delete | api: global_delete | auth: admin
name: str (*req)
No documentation yet.
```

### Global Sentinel Set
```
cli: global sentinel set | api: global_sentinel_set | auth: admin
snt: Sentinel (None)
No documentation yet.
```

### Global Sentinel Unset
```
cli: global sentinel unset | api: global_sentinel_unset | auth: admin
n/a
No documentation yet.
```

## APIs for graph

No documentation yet.

### Graph Create
```
cli: graph create | api: graph_create | auth: user
set_active: bool (True)
No documentation yet.
```

### Graph Get
```
cli: graph get | api: graph_get | auth: user
nd: Node (None), mode: str (default), detailed: bool (False), depth: int (0)
Valid modes: {default, dot, }
```

### Graph List
```
cli: graph list | api: graph_list | auth: user
detailed: bool (False)
No documentation yet.
```

### Graph Active Set
```
cli: graph active set | api: graph_active_set | auth: user
gph: Graph (*req)
No documentation yet.
```

### Graph Active Unset
```
cli: graph active unset | api: graph_active_unset | auth: user
n/a
No documentation yet.
```

### Graph Active Get
```
cli: graph active get | api: graph_active_get | auth: user
detailed: bool (False)
No documentation yet.
```

### Graph Delete
```
cli: graph delete | api: graph_delete | auth: user
gph: Graph (*req)
No documentation yet.
```

### Graph Node Get
```
cli: graph node get | api: graph_node_get | auth: user
nd: Node (*req), keys: list ([])
No documentation yet.
```

### Graph Node View
```
cli: graph node view | api: graph_node_view | auth: user
nd: Node (None), detailed: bool (False), show_edges: bool (False), node_type: str (), edge_type: str ()
No documentation yet.
```

### Graph Node Set
```
cli: graph node set | api: graph_node_set | auth: user
nd: Node (*req), ctx: dict (*req)
No documentation yet.
```

### Graph Walk
```
cli: graph walk (cli only)
nd: Node (None)
No documentation yet.
```

## APIs for jac

No documentation yet.

### Jac Build
```
cli: jac build (cli only)
file: str (*req), out: str (), opt_level: int (4)
No documentation yet.
```

### Jac Disas
```
cli: jac disas (cli only)
file: str (*req)
and .jir executables
```

### Jac Test
```
cli: jac test (cli only)
file: str (*req), single: str (), profiling: bool (False), detailed: bool (False)
and .jir executables
```

### Jac Run
```
cli: jac run (cli only)
file: str (*req), walk: str (init), ctx: dict ({}), profiling: bool (False)
and .jir executables
```

### Jac Dot
```
cli: jac dot (cli only)
file: str (*req), walk: str (init), ctx: dict ({}), detailed: bool (False)
files and .jir executables
```

## APIs for js_orc

No documentation yet.

### Load Yaml
```
cli: load yaml | api: load_yaml | auth: admin
files: list (*req), namespace: str (default)
No documentation yet.
```

### Apply Yaml
```
cli: apply yaml | api: apply_yaml | auth: admin
name: str (*req), file: list (*req), unsafe_paraphrase: str ()
No documentation yet.
```

### Service Refresh
```
cli: service refresh | api: service_refresh | auth: admin
name: str (*req)
No documentation yet.
```

### Service Call
```
cli: service call | api: service_call | auth: admin
svc: str (*req), attrs: list ([])
No documentation yet.
```
### Jsorc Actions Load
```
cli: jsorc actions load | api: jsorc_actions_load | auth: admin
name: str (*req), mode: str (*req)
JSORC will load the corresponding module or start a microservice if needed. Return the current status of the action.
```

### Jsorc Actions Status
```
cli: jsorc actions status | api: jsorc_actions_status | auth: admin
name: str (*req)
No documentation yet.
```

### Jsorc Actions Unload
```
cli: jsorc actions unload | api: jsorc_actions_unload | auth: admin
name: str (*req), mode: str (auto), retire_svc: bool (True)
If retire svc is set to True (true by default), it will also retire the corresponding microservice.
```

### Jsorc Actions Config
```
cli: jsorc actions config | api: jsorc_actions_config | auth: admin
config: str (*req), name: str (*req)
config: name of the ai kit package (e.g. jac nlp.config, jac vision.config) name: name of the action module (e.g. use enc, bi enc)
```

### Jsorc Trackact Start
```
cli: jsorc trackact start | api: jsorc_trackact_start | auth: admin
n/a
Instruct JSORC to start tracking any changes in actions state
```

### Jsorc Trackact Stop
```
cli: jsorc trackact stop | api: jsorc_trackact_stop | auth: admin
n/a
Instruct JSORC to start tracking any changes in actions state
```

### Jsorc Benchmark Start
```
cli: jsorc benchmark start | api: jsorc_benchmark_start | auth: admin
n/a
No documentation yet.
```

### Jsorc Benchmark Report
```
cli: jsorc benchmark report | api: jsorc_benchmark_report | auth: admin
n/a
No documentation yet.
```

### Jsorc Benchmark Stop
```
cli: jsorc benchmark stop | api: jsorc_benchmark_stop | auth: admin
report: bool (True)
No documentation yet.
```

### Jsorc Tracksys Start
```
cli: jsorc tracksys start | api: jsorc_tracksys_start | auth: admin
n/a
No documentation yet.
```

### Jsorc Tracksys Report
```
cli: jsorc tracksys report | api: jsorc_tracksys_report | auth: admin
n/a
No documentation yet.
```

### Jsorc Tracksys Stop
```
cli: jsorc tracksys stop | api: jsorc_tracksys_stop | auth: admin
n/a
No documentation yet.
```
### Jsorc Actionpolicy Set
```
cli: jsorc actionpolicy set | api: jsorc_actionpolicy_set | auth: admin
policy_name: str (*req), policy_params: dict ({})
No documentation yet.
```

### Jsorc Actionpolicy Get
```
cli: jsorc actionpolicy get | api: jsorc_actionpolicy_get | auth: admin
n/a
No documentation yet.
```

### Jsorc Loadtest
```
cli: jsorc loadtest | api: jsorc_loadtest | auth: admin
test: str (*req), experiment: str (), mem: int (0)
No documentation yet.
```

## APIs for logger

No documentation yet.

### Logger Http Connect
```
cli: logger http connect | api: logger_http_connect | auth: admin
host: str (*req), port: int (*req), url: str (*req), log: str (all)
Valid log params: {sys, app, all }
```

### Logger Http Clear
```
cli: logger http clear | api: logger_http_clear | auth: admin
log: str (all)
Valid log params: {sys, app, all }
```

### Logger Get
```
cli: logger get | api: logger_get | auth: admin
search: str (), level: str (None)
No documentation yet.
```

### Logger List
```
cli: logger list | api: logger_list | auth: admin
n/a
No documentation yet.
```

## APIs for master

### Master Create
```
cli: master create | api: master_create | auth: user
name: str (*req), password: str (), global_init: str (), global_init_ctx: dict ({}), other_fields: dict ({})
other fields used for additional feilds for overloaded interfaces (i.e., Dango interface)
```

### Master Get
```
cli: master get | api: master_get | auth: user
name: str (*req), mode: str (default), detailed: bool (False)
Valid modes: {default, }
```

### Master List
```
cli: master list | api: master_list | auth: user
detailed: bool (False)
No documentation yet.
```

### Master Active Set
```
cli: master active set | api: master_active_set | auth: user
name: str (*req)
NOTE: Specail handler included in general interface to api
```

### Master Active Unset
```
cli: master active unset | api: master_active_unset | auth: user
n/a
No documentation yet.
```

### Master Active Get
```
cli: master active get | api: master_active_get | auth: user
detailed: bool (False)
No documentation yet.
```

### Master Self
```
cli: master self | api: master_self | auth: user
detailed: bool (False)
No documentation yet.
```

### Master Delete
```
cli: master delete | api: master_delete | auth: user
name: str (*req)
No documentation yet.
```

## APIs for object

### Global Get
```
cli: global get | api: global_get | auth: user
name: str (*req)
No documentation yet.
```

### Object Get
```
cli: object get | api: object_get | auth: user
obj: Element (*req), depth: int (0), detailed: bool (False)
No documentation yet.
```

### Object Perms Get
```
cli: object perms get | api: object_perms_get | auth: user
obj: Element (*req)
No documentation yet.
```

### Object Perms Set
```
cli: object perms set | api: object_perms_set | auth: user
obj: Element (*req), mode: str (*req)
No documentation yet.
```

### Object Perms Default
```
cli: object perms default | api: object_perms_default | auth: user
mode: str (*req)
No documentation yet.
```

### Object Perms Grant
```
cli: object perms grant | api: object_perms_grant | auth: user
obj: Element (*req), mast: Element (*req), read_only: bool (False)
No documentation yet.
```

### Object Perms Revoke
```
cli: object perms revoke | api: object_perms_revoke | auth: user
obj: Element (*req), mast: Element (*req)
No documentation yet.
```

### Info
```
cli: info | api: info | auth: public
n/a
No documentation yet.
```

## APIs for prometheus

No documentation yet.

### Prometheus Metrics List
```
cli: prometheus metrics list | api: prometheus_metrics_list | auth: admin
n/a
No documentation yet.
```

### Prometheus Pod List
```
cli: prometheus pod list | api: prometheus_pod_list | auth: admin
namespace: str (), exclude_prom: bool (False)
No documentation yet.
```

### Prometheus Pod Info
```
cli: prometheus pod info | api: prometheus_pod_info | auth: admin
namespace: str (), exclude_prom: bool (False), timestamp: int (0), duration: int (0)
No documentation yet.
```

## APIs for queue

APIs used for celery configuration and monitoring

### Walker Queue Check
```
cli: walker queue check | api: walker_queue_check | auth: user
task_id: str ()
No documentation yet.
```

### Walker Queue Wait
```
cli: walker queue wait | api: walker_queue_wait | auth: user
task_id: str (*req), timeout: int (30)
No documentation yet.
```

## APIs for sentinel

A sentinel is a unit in Jaseci that represents the organization and management of a collection of architypes and walkers. In a sense, you can think of a sentinel as a complete Jac implementation of a program or API application. Though its the case that many sentinels can be interchangeably across any set of graphs, most use cases will typically be a single sentinel shared by all users and managed by an admin(s), or each users maintaining a single sentinel customized for their individual needs. Many novel usage models are possible, but I'd point the beginner to the model most analogous to typical server side software development to start with. This model would be to have a single admin account responsible for updating a single sentinel that all users would share for their individual graphs. This model is achieved through using \texttt{sentinel_register}, \texttt{sentinel_active_global}, and \texttt{global_sentinel_set}.

### Sentinel Register
```
cli: sentinel register | api: sentinel_register | auth: user
name: str (default), code: str (), code_dir: str (./), opt_level: int (4), mode: str (default), encoded: bool (False), auto_run: str (init), auto_run_ctx: dict ({}), auto_create_graph: bool (True), set_active: bool (True)
Auto run is the walker to execute on register (assumes active graph is selected)
```

### Sentinel Pull
```
cli: sentinel pull | api: sentinel_pull | auth: user
set_active: bool (True), on_demand: bool (True)
No documentation yet.
```

### Sentinel Get
```
cli: sentinel get | api: sentinel_get | auth: user
snt: Sentinel (None), mode: str (default), detailed: bool (False)
Valid modes: {default, code, ir, }
```

### Sentinel Set
```
cli: sentinel set | api: sentinel_set | auth: user
code: str (*req), code_dir: str (./), opt_level: int (4), encoded: bool (False), snt: Sentinel (None), mode: str (default)
Valid modes: {code, ir, }
```

### Sentinel List
```
cli: sentinel list | api: sentinel_list | auth: user
detailed: bool (False)
No documentation yet.
```

### Sentinel Test
```
cli: sentinel test | api: sentinel_test | auth: user
snt: Sentinel (None), single: str (), detailed: bool (False), profiling: bool (False)
No documentation yet.
```

### Sentinel Active Set
```
cli: sentinel active set | api: sentinel_active_set | auth: user
snt: Sentinel (*req)
No documentation yet.
```

### Sentinel Active Unset
```
cli: sentinel active unset | api: sentinel_active_unset | auth: user
n/a
No documentation yet.
```

### Sentinel Active Global
```
cli: sentinel active global | api: sentinel_active_global | auth: user
auto_run: str (), auto_run_ctx: dict ({}), auto_create_graph: bool (False), detailed: bool (False)
Exclusive OR with pull strategy
```

### Sentinel Active Get
```
cli: sentinel active get | api: sentinel_active_get | auth: user
detailed: bool (False)
No documentation yet.
```

### Sentinel Delete
```
cli: sentinel delete | api: sentinel_delete | auth: user
snt: Sentinel (*req)
No documentation yet.
```

## APIs for super

No documentation yet.

### Master Createsuper
```
cli: master createsuper | api: master_createsuper | auth: admin
name: str (*req), password: str (), global_init: str (), global_init_ctx: dict ({}), other_fields: dict ({})
other fields used for additional feilds for overloaded interfaces (i.e., Dango interface)
```

### Master Allusers
```
cli: master allusers | api: master_allusers | auth: admin
limit: int (0), offset: int (0), asc: bool (False), search: str (None)
return and offset specfies where to start NOTE: Abstract interface to be overridden
```

### Master Become
```
cli: master become | api: master_become | auth: admin
mast: Master (*req)
No documentation yet.
```

### Master Unbecome
```
cli: master unbecome | api: master_unbecome | auth: admin
n/a
No documentation yet.
```

## APIs for user

These User APIs enable the creation and management of users on a Jaseci machine. The creation of a user in this context is synonymous to the creation of a master Jaseci object. These APIs are particularly useful when running a Jaseci server or cluster in contrast to running JSCTL on the command line. Upon executing JSCTL a dummy admin user (super_master) is created and all state is dumped to a session file, though any users created during a JSCTL session will indeed be created as part of that session's state.

### User Create
```
cli: user create | api: user_create | auth: public
name: str (*req), password: str (), global_init: str (), global_init_ctx: dict ({}), other_fields: dict ({})
```

This API is used to create users and optionally set them up with a graph and related initialization. In the context of JSCTL, any name is sufficient and no additional information is required. However, for Jaseci serving (whether it be the official Jaseci server, or a custom overloaded server) additional fields are required and should be added to the other fields parameter as per the specifics of the encapsulating server requirements. In the case of the official Jaseci server, the name field must be a valid email, and a password field must be passed through other fields. A number of other optional parameters can also be passed through other feilds. \vspace{3mm}\par This single API call can also be used to fully set up and initialize a user by leveraging the global init parameter. When set, this parameter attaches the user to the global sentinel, creates a new graph for the user, sets it as the active graph, then runs an initialization walker on the root node of this new graph. The initialization walker is identified by the name assigned to global init. The default empty string assigned to global init indicates this global setup should not be run.

#### Params
**Params name** -- The user name to create. For Jaseci server this must be a valid email address.
**global_init** -- The name of an initialization walker. When set the user is linked to the global sentinel and the walker is run on a new active graph created for the user.
**global_init_ctx** -- Context to preload for the initialization walker
**other_fields** -- This parameter is used for additional fields required for overloaded interfaces. This parameter is not used in JSCTL, but is used by Jaseci server for the additional parameters of password, is_activated, and is_superuser.

### User Delete
```
cli: user delete | api: user_delete | auth: admin
name: str (*req)
This API is used to delete a user account.
```
#### Params
**Params name** -- The user name to delete. For Jaseci server this must be a valid email address.

### User Deleteself
```
cli: user deleteself | api: user_deleteself | auth: user
n/a
This API is used to delete a user account.
```


## APIs for walker

The walker set of APIs are used for execution and management of walkers. Walkers are the primary entry points for running Jac programs. The primary API used to run walkers is \textbf{walker_run}. There are a number of variations on this API that enable the invocation of walkers with various semantics.

### Walker Get
```
cli: walker get | api: walker_get | auth: user
wlk: Walker (*req), mode: str (default), detailed: bool (False)
Valid modes: {default, code, ir, keys, }
```

### Walker Total
```
cli: walker total | api: walker_total | auth: user
snt: Sentinel (None), detailed: bool (False)
No documentation yet.
```

### Walker List
```
cli: walker list | api: walker_list | auth: user
snt: Sentinel (None), detailed: bool (False)
No documentation yet.
```

### Walker Spawn Create
```
cli: walker spawn create | api: walker_spawn_create | auth: user
name: str (*req), snt: Sentinel (None)
No documentation yet.
```

### Walker Spawn List
```
cli: walker spawn list | api: walker_spawn_list | auth: user
detailed: bool (False)
No documentation yet.
```

### Walker Spawn Delete
```
cli: walker spawn delete | api: walker_spawn_delete | auth: user
name: str (*req)
No documentation yet.
```

### Walker Spawn Clear
```
cli: walker spawn clear | api: walker_spawn_clear | auth: user
n/a
No documentation yet.
```

### Walker Yield List
```
cli: walker yield list | api: walker_yield_list | auth: user
detailed: bool (False)
No documentation yet.
```

### Walker Yield Delete
```
cli: walker yield delete | api: walker_yield_delete | auth: user
name: str (*req)
No documentation yet.
```

### Walker Yield Clear
```
cli: walker yield clear | api: walker_yield_clear | auth: user
n/a
No documentation yet.
```

### Walker Prime
```
cli: walker prime | api: walker_prime | auth: user
wlk: Walker (*req), nd: Node (None), ctx: dict ({}), _req_ctx: dict ({})
No documentation yet.
```

### Walker Execute
```
cli: walker execute | api: walker_execute | auth: user
wlk: Walker (*req), prime: Node (None), ctx: dict ({}), _req_ctx: dict ({}), profiling: bool (False)
No documentation yet.
```

### Walker Run
```
cli: walker run | api: walker_run | auth: user
name: str (*req), nd: Node (None), ctx: dict ({}), _req_ctx: dict ({}), snt: Sentinel (None), profiling: bool (False), is_async: bool (None)
reports results, and cleans up walker instance.
```

### Wapi
```
cli: wapi | api: wapi | auth: user
name: str (*req), nd: Node (None), ctx: dict ({}), _req_ctx: dict ({}), snt: Sentinel (None), profiling: bool (False)
No documentation yet.
```

### Walker Summon
```
cli: walker summon | api: walker_summon | auth: public
key: str (*req), wlk: Walker (*req), nd: Node (*req), ctx: dict ({}), _req_ctx: dict ({}), global_sync: bool (True)
along with the walker id and node id
```

### Walker Callback
```
cli: walker callback | api: walker_callback | auth: public
nd: Node (*req), wlk: Walker (*req), key: str (*req), ctx: dict ({}), _req_ctx: dict ({}), global_sync: bool (True)
along with the walker id and node id
```

## APIs for webhook

No documentation yet.

### Webhook

```
cli: webhook | api: webhook | auth: public
provider: str (*req), _req_ctx: dict ({}), _raw_req_ctx: str (None)
No documentation yet.
```

## APIs for apps_v1

Ref: https://openapi-generator.tech
Do not edit the class manually.


## APIs for core_v1

Ref: https://openapi-generator.tech
Do not edit the class manually.


## APIs for rbac_authorization_v1

Ref: https://openapi-generator.tech
Do not edit the class manually.