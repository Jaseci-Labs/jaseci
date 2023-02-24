 # APIs for actions

This set action APIs enable the manual management of Jaseci actions and action
libraries/sets. Action libraries can be loaded locally into the running instance of
the python program, or as a remote container linked action library. In this mode,
action libraries operate as micro-services. Jaseci will be able to dynamically
and automatically make this decision for the user based on online monitoring and
performance profiling.

<div class='actionHeading'>actions load local</div>

 <div class='actionName'> cli: actions load local | api: actions_load_local | auth: admin </div> 
 <div class ='actionsArgs'> file: str (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>This API will dynamically load a module based on a python file. The module
is loaded directly into the running Jaseci python instance. This API also
makes an attempt to auto detect and hot load any python package dependencies
the file may reference via python's relative imports. This file is assumed to
have the necessary annotations and decorations required by Jaseci to recognize
its actions.<div class='heading'>Params</div> 
 <div class='params'> Params 
file -- The python file with full to load actions from.
(i.e., ~/local/myact.py) <br> 
</div></div> </div> 
 
<div class='actionHeading'>actions load remote</div>

 <div class='actionName'> cli: actions load remote | api: actions_load_remote | auth: admin </div> 
 <div class ='actionsArgs'> url: str (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>This API will dynamically load a set of actions that are present on a remote
server/micro-service. This server must be configured to interact with Jaseci
properly. This is easily achieved using the same decorators used for local
action libraries. Remote actions allow for higher flexibility in the languages
supported for action libraries. If an  library writer would like to use another
language, the main hook REST api simply needs to be implemented. Please
refer to documentation on creating action libraries for more details.<div class='heading'>Params</div> 
 <div class='params'> Params 
url -- The url of the API server supporting Jaseci actions. <br> 
</div></div> </div> 
 
<div class='actionHeading'>actions load module</div>

 <div class='actionName'> cli: actions load module | api: actions_load_module | auth: admin </div> 
 <div class ='actionsArgs'> mod: str (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>This API will dynamically load a module using python's module import format.
This is particularly useful for pip installed action libraries as the developer
can directly reference the module using the same format as a regular python
import. As with load local, the module will be loaded directly into the running
Jaseci python instance.<div class='heading'>Params</div> 
 <div class='params'> Params 
mod -- The import style module to load actions from.
(i.e., jaseci_ai_kit.bi_enc) <br> 
</div></div> </div> 
 
<div class='actionHeading'>actions list</div>

 <div class='actionName'> cli: actions list | api: actions_list | auth: admin </div> 
 <div class ='actionsArgs'> name: str ()</div>
 <div class ='mainbody'> <div class ='actionsDescription'>This API is used to list the loaded actions active in Jaseci. These actions
include all types of loaded actions whether it be local modules or remote
containers. A particular set of actions can be viewed using the name parameter.<div class='heading'>Params</div> 
 <div class='params'> Params 
name -- The name for a library for which to filter the view of shown
actions. If left blank all actions from all loaded sets will be shown. <br> 
</div></div> </div> 
 
<div class='actionHeading'>actions module list</div>

 <div class='actionName'> cli: actions module list | api: actions_module_list | auth: admin </div> 
 <div class ='actionsArgs'> detailed: bool (False)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>actions unload module</div>

 <div class='actionName'> cli: actions unload module | api: actions_unload_module | auth: admin </div> 
 <div class ='actionsArgs'> name: str (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>actions unload action</div>

 <div class='actionName'> cli: actions unload action | api: actions_unload_action | auth: admin </div> 
 <div class ='actionsArgs'> name: str (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>actions unload actionset</div>

 <div class='actionName'> cli: actions unload actionset | api: actions_unload_actionset | auth: admin </div> 
 <div class ='actionsArgs'> name: str (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 # APIs for architype

The architype set of APIs allow for the addition and removing of
architypes. Given a Jac implementation of an architype these APIs are
designed for creating, compiling, and managing architypes that can be
used by Jaseci. There are two ways to add an architype to Jaseci, either
through the management of sentinels using the sentinel API, or by
registering independent architypes with these architype APIs. These
APIs are also used for inspecting and managing existing arichtypes that
a Jaseci instance is aware of.

<div class='actionHeading'>architype register</div>

 <div class='actionName'> cli: architype register | api: architype_register | auth: user </div> 
 <div class ='actionsArgs'> code: str (*req), encoded: bool (False), snt: Sentinel (None)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>This register API allows for the creation or replacement/update of
an architype that can then be used by walkers in their interactions
of graphs. The code argument takes Jac source code for the single
architype. To load multiple architypes and walkers at the same time,
use sentinel register API.<div class='heading'>Params</div> 
 <div class='params'> Params 
code -- The text (or filename) for an architypes Jac code <br> 

encoded -- True/False flag as to whether code is encode
in base64 <br> 

snt -- The UUID of the sentinel to be the owner of this
architype <br> 
</div><div class='heading'>Returns</div> 
<div class='return'>Returns - Fields include
'architype': Architype object if created otherwise null
'success': True/False whether register was successful
'errors': List of errors if register failed
'response': Message on outcome of register call</div> </div> 
 
<div class='actionHeading'>architype get</div>

 <div class='actionName'> cli: architype get | api: architype_get | auth: user </div> 
 <div class ='actionsArgs'> arch: Architype (*req), mode: str (default), detailed: bool (False)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.<div class='heading'>Params</div> 
 <div class='params'> Params 
arch -- The architype being accessed <br> 

mode -- Valid modes: {default, code, ir, } <br> 

detailed -- Flag to give summary or complete set of fields <br> 
</div><div class='heading'>Returns</div> 
<div class='return'>Returns - Fields include (depends on mode)
'code': Formal source code for architype
'ir': Intermediate representation of architype
'architype': Architype object print</div> </div> 
 
<div class='actionHeading'>architype set</div>

 <div class='actionName'> cli: architype set | api: architype_set | auth: user </div> 
 <div class ='actionsArgs'> arch: Architype (*req), code: str (*req), mode: str (default)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.<div class='heading'>Params</div> 
 <div class='params'> Params 
arch -- The architype being set <br> 

code -- The text (or filename) for an architypes Jac code/ir <br> 

mode -- Valid modes: {default, code, ir, } <br> 
</div><div class='heading'>Returns</div> 
<div class='return'>Returns - Fields include (depends on mode)
'success': True/False whether set was successful
'errors': List of errors if set failed
'response': Message on outcome of set call</div> </div> 
 
<div class='actionHeading'>architype list</div>

 <div class='actionName'> cli: architype list | api: architype_list | auth: user </div> 
 <div class ='actionsArgs'> snt: Sentinel (None), kind: str (None), detailed: bool (False)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.<div class='heading'>Params</div> 
 <div class='params'> Params 
snt -- The sentinel for which to list its architypes <br> 

detailed -- Flag to give summary or complete set of fields <br> 

kind -- Architype kind used to narrow the result set <br> 
</div><div class='heading'>Returns</div> 
<div class='return'>Returns - List of architype objects</div> </div> 
 
<div class='actionHeading'>architype count</div>

 <div class='actionName'> cli: architype count | api: architype_count | auth: user </div> 
 <div class ='actionsArgs'> snt: Sentinel (None), kind: str (None)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.<div class='heading'>Params</div> 
 <div class='params'> Params 
snt -- The sentinel for which to list its architypes <br> 

detailed -- Flag to give summary or complete set of fields <br> 

kind -- Architype kind used to narrow the result set from which the count is evaluated <br> 
</div><div class='heading'>Returns</div> 
<div class='return'>Returns - Count of architype objects</div> </div> 
 
<div class='actionHeading'>architype delete</div>

 <div class='actionName'> cli: architype delete | api: architype_delete | auth: user </div> 
 <div class ='actionsArgs'> arch: Architype (*req), snt: Sentinel (None)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.<div class='heading'>Params</div> 
 <div class='params'> Params 
arch -- The architype being set <br> 

snt -- The sentinel for which to list its architypes <br> 
</div><div class='heading'>Returns</div> 
<div class='return'>Returns - Fields include (depends on mode)
'success': True/False whether command was successful
'response': Message on outcome of command</div> </div> 
 
 # APIs for config

Abstracted since there are no valid configs in core atm, see jaseci\_serv
to see how used.

<div class='actionHeading'>config get</div>

 <div class='actionName'> cli: config get | api: config_get | auth: admin </div> 
 <div class ='actionsArgs'> name: str (*req), do_check: bool (True)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>config set</div>

 <div class='actionName'> cli: config set | api: config_set | auth: admin </div> 
 <div class ='actionsArgs'> name: str (*req), value: str (*req), do_check: bool (True)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>config list</div>

 <div class='actionName'> cli: config list | api: config_list | auth: admin </div> 
 <div class ='actionsArgs'> n/a</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>config index</div>

 <div class='actionName'> cli: config index | api: config_index | auth: admin </div> 
 <div class ='actionsArgs'> n/a</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>config exists</div>

 <div class='actionName'> cli: config exists | api: config_exists | auth: admin </div> 
 <div class ='actionsArgs'> name: str (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>config delete</div>

 <div class='actionName'> cli: config delete | api: config_delete | auth: admin </div> 
 <div class ='actionsArgs'> name: str (*req), do_check: bool (True)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 # APIs for global

No documentation yet.

<div class='actionHeading'>global set</div>

 <div class='actionName'> cli: global set | api: global_set | auth: admin </div> 
 <div class ='actionsArgs'> name: str (*req), value: str (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>global delete</div>

 <div class='actionName'> cli: global delete | api: global_delete | auth: admin </div> 
 <div class ='actionsArgs'> name: str (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>global sentinel set</div>

 <div class='actionName'> cli: global sentinel set | api: global_sentinel_set | auth: admin </div> 
 <div class ='actionsArgs'> snt: Sentinel (None)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>global sentinel unset</div>

 <div class='actionName'> cli: global sentinel unset | api: global_sentinel_unset | auth: admin </div> 
 <div class ='actionsArgs'> n/a</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 # APIs for graph

No documentation yet.

<div class='actionHeading'>graph create</div>

 <div class='actionName'> cli: graph create | api: graph_create | auth: user </div> 
 <div class ='actionsArgs'> set_active: bool (True)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>graph get</div>

 <div class='actionName'> cli: graph get | api: graph_get | auth: user </div> 
 <div class ='actionsArgs'> nd: Node (None), mode: str (default), detailed: bool (False), depth: int (0)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>Valid modes: {default, dot, }</div> </div> 
 
<div class='actionHeading'>graph list</div>

 <div class='actionName'> cli: graph list | api: graph_list | auth: user </div> 
 <div class ='actionsArgs'> detailed: bool (False)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>graph active set</div>

 <div class='actionName'> cli: graph active set | api: graph_active_set | auth: user </div> 
 <div class ='actionsArgs'> gph: Graph (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>graph active unset</div>

 <div class='actionName'> cli: graph active unset | api: graph_active_unset | auth: user </div> 
 <div class ='actionsArgs'> n/a</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>graph active get</div>

 <div class='actionName'> cli: graph active get | api: graph_active_get | auth: user </div> 
 <div class ='actionsArgs'> detailed: bool (False)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>graph delete</div>

 <div class='actionName'> cli: graph delete | api: graph_delete | auth: user </div> 
 <div class ='actionsArgs'> gph: Graph (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>graph node get</div>

 <div class='actionName'> cli: graph node get | api: graph_node_get | auth: user </div> 
 <div class ='actionsArgs'> nd: Node (*req), keys: list ([])</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>graph node view</div>

 <div class='actionName'> cli: graph node view | api: graph_node_view | auth: user </div> 
 <div class ='actionsArgs'> nd: Node (None), detailed: bool (False), show_edges: bool (False), node_type: str (), edge_type: str ()</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>graph node set</div>

 <div class='actionName'> cli: graph node set | api: graph_node_set | auth: user </div> 
 <div class ='actionsArgs'> nd: Node (*req), ctx: dict (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>graph walk</div>

 <div class='actionName'> cli: graph walk (cli only) </div> 
 <div class ='actionsArgs'> nd: Node (None)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 # APIs for jac

No documentation yet.

<div class='actionHeading'>jac build</div>

 <div class='actionName'> cli: jac build (cli only) </div> 
 <div class ='actionsArgs'> file: str (*req), out: str (), opt_level: int (4)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>jac disas</div>

 <div class='actionName'> cli: jac disas (cli only) </div> 
 <div class ='actionsArgs'> file: str (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>and .jir executables</div> </div> 
 
<div class='actionHeading'>jac test</div>

 <div class='actionName'> cli: jac test (cli only) </div> 
 <div class ='actionsArgs'> file: str (*req), single: str (), profiling: bool (False), detailed: bool (False)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>and .jir executables</div> </div> 
 
<div class='actionHeading'>jac run</div>

 <div class='actionName'> cli: jac run (cli only) </div> 
 <div class ='actionsArgs'> file: str (*req), walk: str (init), ctx: dict ({}), profiling: bool (False)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>and .jir executables</div> </div> 
 
<div class='actionHeading'>jac dot</div>

 <div class='actionName'> cli: jac dot (cli only) </div> 
 <div class ='actionsArgs'> file: str (*req), walk: str (init), ctx: dict ({}), detailed: bool (False)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>files and .jir executables</div> </div> 
 
 # APIs for js_orc

No documentation yet.

<div class='actionHeading'>load yaml</div>

 <div class='actionName'> cli: load yaml | api: load_yaml | auth: admin </div> 
 <div class ='actionsArgs'> files: list (*req), namespace: str (default)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>apply yaml</div>

 <div class='actionName'> cli: apply yaml | api: apply_yaml | auth: admin </div> 
 <div class ='actionsArgs'> name: str (*req), file: list (*req), unsafe_paraphrase: str ()</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>service refresh</div>

 <div class='actionName'> cli: service refresh | api: service_refresh | auth: admin </div> 
 <div class ='actionsArgs'> name: str (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>service call</div>

 <div class='actionName'> cli: service call | api: service_call | auth: admin </div> 
 <div class ='actionsArgs'> svc: str (*req), attrs: list ([])</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>jsorc actions load</div>

 <div class='actionName'> cli: jsorc actions load | api: jsorc_actions_load | auth: admin </div> 
 <div class ='actionsArgs'> name: str (*req), mode: str (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>JSORC will load the corresponding module or start a microservice if needed.
Return the current status of the action.</div> </div> 
 
<div class='actionHeading'>jsorc actions status</div>

 <div class='actionName'> cli: jsorc actions status | api: jsorc_actions_status | auth: admin </div> 
 <div class ='actionsArgs'> name: str (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>jsorc actions unload</div>

 <div class='actionName'> cli: jsorc actions unload | api: jsorc_actions_unload | auth: admin </div> 
 <div class ='actionsArgs'> name: str (*req), mode: str (auto), retire_svc: bool (True)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>If retire svc is set to True (true by default), it will also retire the corresponding microservice.</div> </div> 
 
<div class='actionHeading'>jsorc actions config</div>

 <div class='actionName'> cli: jsorc actions config | api: jsorc_actions_config | auth: admin </div> 
 <div class ='actionsArgs'> config: str (*req), name: str (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>config: name of the ai kit package (e.g. jac nlp.config, jac vision.config)
name: name of the action module (e.g. use enc, bi enc)</div> </div> 
 
<div class='actionHeading'>jsorc trackact start</div>

 <div class='actionName'> cli: jsorc trackact start | api: jsorc_trackact_start | auth: admin </div> 
 <div class ='actionsArgs'> n/a</div>
 <div class ='mainbody'> <div class ='actionsDescription'>Instruct JSORC to start tracking any changes in actions state</div> </div> 
 
<div class='actionHeading'>jsorc trackact stop</div>

 <div class='actionName'> cli: jsorc trackact stop | api: jsorc_trackact_stop | auth: admin </div> 
 <div class ='actionsArgs'> n/a</div>
 <div class ='mainbody'> <div class ='actionsDescription'>Instruct JSORC to start tracking any changes in actions state</div> </div> 
 
<div class='actionHeading'>jsorc benchmark start</div>

 <div class='actionName'> cli: jsorc benchmark start | api: jsorc_benchmark_start | auth: admin </div> 
 <div class ='actionsArgs'> n/a</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>jsorc benchmark report</div>

 <div class='actionName'> cli: jsorc benchmark report | api: jsorc_benchmark_report | auth: admin </div> 
 <div class ='actionsArgs'> n/a</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>jsorc benchmark stop</div>

 <div class='actionName'> cli: jsorc benchmark stop | api: jsorc_benchmark_stop | auth: admin </div> 
 <div class ='actionsArgs'> report: bool (True)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>jsorc tracksys start</div>

 <div class='actionName'> cli: jsorc tracksys start | api: jsorc_tracksys_start | auth: admin </div> 
 <div class ='actionsArgs'> n/a</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>jsorc tracksys report</div>

 <div class='actionName'> cli: jsorc tracksys report | api: jsorc_tracksys_report | auth: admin </div> 
 <div class ='actionsArgs'> n/a</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>jsorc tracksys stop</div>

 <div class='actionName'> cli: jsorc tracksys stop | api: jsorc_tracksys_stop | auth: admin </div> 
 <div class ='actionsArgs'> n/a</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>jsorc actionpolicy set</div>

 <div class='actionName'> cli: jsorc actionpolicy set | api: jsorc_actionpolicy_set | auth: admin </div> 
 <div class ='actionsArgs'> policy_name: str (*req), policy_params: dict ({})</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>jsorc actionpolicy get</div>

 <div class='actionName'> cli: jsorc actionpolicy get | api: jsorc_actionpolicy_get | auth: admin </div> 
 <div class ='actionsArgs'> n/a</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>jsorc loadtest</div>

 <div class='actionName'> cli: jsorc loadtest | api: jsorc_loadtest | auth: admin </div> 
 <div class ='actionsArgs'> test: str (*req), experiment: str (), mem: int (0)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 # APIs for logger

No documentation yet.

<div class='actionHeading'>logger http connect</div>

 <div class='actionName'> cli: logger http connect | api: logger_http_connect | auth: admin </div> 
 <div class ='actionsArgs'> host: str (*req), port: int (*req), url: str (*req), log: str (all)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>Valid log params: {sys, app, all }</div> </div> 
 
<div class='actionHeading'>logger http clear</div>

 <div class='actionName'> cli: logger http clear | api: logger_http_clear | auth: admin </div> 
 <div class ='actionsArgs'> log: str (all)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>Valid log params: {sys, app, all }</div> </div> 
 
<div class='actionHeading'>logger get</div>

 <div class='actionName'> cli: logger get | api: logger_get | auth: admin </div> 
 <div class ='actionsArgs'> search: str (), level: str (None)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>logger list</div>

 <div class='actionName'> cli: logger list | api: logger_list | auth: admin </div> 
 <div class ='actionsArgs'> n/a</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 # APIs for master

These APIs

<div class='actionHeading'>master create</div>

 <div class='actionName'> cli: master create | api: master_create | auth: user </div> 
 <div class ='actionsArgs'> name: str (*req), password: str (), global_init: str (), global_init_ctx: dict ({}), other_fields: dict ({})</div>
 <div class ='mainbody'> <div class ='actionsDescription'>other fields used for additional feilds for overloaded interfaces
(i.e., Dango interface)</div> </div> 
 
<div class='actionHeading'>master get</div>

 <div class='actionName'> cli: master get | api: master_get | auth: user </div> 
 <div class ='actionsArgs'> name: str (*req), mode: str (default), detailed: bool (False)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>Valid modes: {default, }</div> </div> 
 
<div class='actionHeading'>master list</div>

 <div class='actionName'> cli: master list | api: master_list | auth: user </div> 
 <div class ='actionsArgs'> detailed: bool (False)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>master active set</div>

 <div class='actionName'> cli: master active set | api: master_active_set | auth: user </div> 
 <div class ='actionsArgs'> name: str (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>NOTE: Specail handler included in general interface to api</div> </div> 
 
<div class='actionHeading'>master active unset</div>

 <div class='actionName'> cli: master active unset | api: master_active_unset | auth: user </div> 
 <div class ='actionsArgs'> n/a</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>master active get</div>

 <div class='actionName'> cli: master active get | api: master_active_get | auth: user </div> 
 <div class ='actionsArgs'> detailed: bool (False)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>master self</div>

 <div class='actionName'> cli: master self | api: master_self | auth: user </div> 
 <div class ='actionsArgs'> detailed: bool (False)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>master delete</div>

 <div class='actionName'> cli: master delete | api: master_delete | auth: user </div> 
 <div class ='actionsArgs'> name: str (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 # APIs for object

...

<div class='actionHeading'>global get</div>

 <div class='actionName'> cli: global get | api: global_get | auth: user </div> 
 <div class ='actionsArgs'> name: str (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>object get</div>

 <div class='actionName'> cli: object get | api: object_get | auth: user </div> 
 <div class ='actionsArgs'> obj: Element (*req), depth: int (0), detailed: bool (False)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>object perms get</div>

 <div class='actionName'> cli: object perms get | api: object_perms_get | auth: user </div> 
 <div class ='actionsArgs'> obj: Element (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>object perms set</div>

 <div class='actionName'> cli: object perms set | api: object_perms_set | auth: user </div> 
 <div class ='actionsArgs'> obj: Element (*req), mode: str (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>object perms default</div>

 <div class='actionName'> cli: object perms default | api: object_perms_default | auth: user </div> 
 <div class ='actionsArgs'> mode: str (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>object perms grant</div>

 <div class='actionName'> cli: object perms grant | api: object_perms_grant | auth: user </div> 
 <div class ='actionsArgs'> obj: Element (*req), mast: Element (*req), read_only: bool (False)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>object perms revoke</div>

 <div class='actionName'> cli: object perms revoke | api: object_perms_revoke | auth: user </div> 
 <div class ='actionsArgs'> obj: Element (*req), mast: Element (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>info</div>

 <div class='actionName'> cli: info | api: info | auth: public </div> 
 <div class ='actionsArgs'> n/a</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 # APIs for prometheus

No documentation yet.

<div class='actionHeading'>prometheus metrics list</div>

 <div class='actionName'> cli: prometheus metrics list | api: prometheus_metrics_list | auth: admin </div> 
 <div class ='actionsArgs'> n/a</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>prometheus pod list</div>

 <div class='actionName'> cli: prometheus pod list | api: prometheus_pod_list | auth: admin </div> 
 <div class ='actionsArgs'> namespace: str (), exclude_prom: bool (False)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>prometheus pod info</div>

 <div class='actionName'> cli: prometheus pod info | api: prometheus_pod_info | auth: admin </div> 
 <div class ='actionsArgs'> namespace: str (), exclude_prom: bool (False), timestamp: int (0), duration: int (0)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 # APIs for queue

APIs used for celery configuration and monitoring

<div class='actionHeading'>walker queue check</div>

 <div class='actionName'> cli: walker queue check | api: walker_queue_check | auth: user </div> 
 <div class ='actionsArgs'> task_id: str ()</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>walker queue wait</div>

 <div class='actionName'> cli: walker queue wait | api: walker_queue_wait | auth: user </div> 
 <div class ='actionsArgs'> task_id: str (*req), timeout: int (30)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 # APIs for sentinel

A sentinel is a unit in Jaseci that represents the organization and management of
a collection of architypes and walkers. In a sense, you can think of a sentinel
as a complete Jac implementation of a program or API application. Though its the
case that many sentinels can be interchangeably across any set of graphs, most
use cases will typically be a single sentinel shared by all users and managed by an
admin(s), or each users maintaining a single sentinel customized for their
individual needs. Many novel usage models are possible, but I'd point the beginner
to the model most analogous to typical server side software development to start
with. This model would be to have a single admin account responsible for updating
a single sentinel that all users would share for their individual graphs. This
model is achieved through using \texttt{sentinel\_register},
\texttt{sentinel\_active\_global}, and \texttt{global\_sentinel\_set}.

<div class='actionHeading'>sentinel register</div>

 <div class='actionName'> cli: sentinel register | api: sentinel_register | auth: user </div> 
 <div class ='actionsArgs'> name: str (default), code: str (), code_dir: str (./), opt_level: int (4), mode: str (default), encoded: bool (False), auto_run: str (init), auto_run_ctx: dict ({}), auto_create_graph: bool (True), set_active: bool (True)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>Auto run is the walker to execute on register (assumes active graph
is selected)</div> </div> 
 
<div class='actionHeading'>sentinel pull</div>

 <div class='actionName'> cli: sentinel pull | api: sentinel_pull | auth: user </div> 
 <div class ='actionsArgs'> set_active: bool (True), on_demand: bool (True)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>sentinel get</div>

 <div class='actionName'> cli: sentinel get | api: sentinel_get | auth: user </div> 
 <div class ='actionsArgs'> snt: Sentinel (None), mode: str (default), detailed: bool (False)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>Valid modes: {default, code, ir, }</div> </div> 
 
<div class='actionHeading'>sentinel set</div>

 <div class='actionName'> cli: sentinel set | api: sentinel_set | auth: user </div> 
 <div class ='actionsArgs'> code: str (*req), code_dir: str (./), opt_level: int (4), encoded: bool (False), snt: Sentinel (None), mode: str (default)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>Valid modes: {code, ir, }</div> </div> 
 
<div class='actionHeading'>sentinel list</div>

 <div class='actionName'> cli: sentinel list | api: sentinel_list | auth: user </div> 
 <div class ='actionsArgs'> detailed: bool (False)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>sentinel test</div>

 <div class='actionName'> cli: sentinel test | api: sentinel_test | auth: user </div> 
 <div class ='actionsArgs'> snt: Sentinel (None), single: str (), detailed: bool (False), profiling: bool (False)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>sentinel active set</div>

 <div class='actionName'> cli: sentinel active set | api: sentinel_active_set | auth: user </div> 
 <div class ='actionsArgs'> snt: Sentinel (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>sentinel active unset</div>

 <div class='actionName'> cli: sentinel active unset | api: sentinel_active_unset | auth: user </div> 
 <div class ='actionsArgs'> n/a</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>sentinel active global</div>

 <div class='actionName'> cli: sentinel active global | api: sentinel_active_global | auth: user </div> 
 <div class ='actionsArgs'> auto_run: str (), auto_run_ctx: dict ({}), auto_create_graph: bool (False), detailed: bool (False)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>Exclusive OR with pull strategy</div> </div> 
 
<div class='actionHeading'>sentinel active get</div>

 <div class='actionName'> cli: sentinel active get | api: sentinel_active_get | auth: user </div> 
 <div class ='actionsArgs'> detailed: bool (False)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>sentinel delete</div>

 <div class='actionName'> cli: sentinel delete | api: sentinel_delete | auth: user </div> 
 <div class ='actionsArgs'> snt: Sentinel (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 # APIs for super

No documentation yet.

<div class='actionHeading'>master createsuper</div>

 <div class='actionName'> cli: master createsuper | api: master_createsuper | auth: admin </div> 
 <div class ='actionsArgs'> name: str (*req), password: str (), global_init: str (), global_init_ctx: dict ({}), other_fields: dict ({})</div>
 <div class ='mainbody'> <div class ='actionsDescription'>other fields used for additional feilds for overloaded interfaces
(i.e., Dango interface)</div> </div> 
 
<div class='actionHeading'>master allusers</div>

 <div class='actionName'> cli: master allusers | api: master_allusers | auth: admin </div> 
 <div class ='actionsArgs'> limit: int (0), offset: int (0), asc: bool (False), search: str (None)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>return and offset specfies where to start
NOTE: Abstract interface to be overridden</div> </div> 
 
<div class='actionHeading'>master become</div>

 <div class='actionName'> cli: master become | api: master_become | auth: admin </div> 
 <div class ='actionsArgs'> mast: Master (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>master unbecome</div>

 <div class='actionName'> cli: master unbecome | api: master_unbecome | auth: admin </div> 
 <div class ='actionsArgs'> n/a</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 # APIs for user

These User APIs enable the creation and management of users on a Jaseci machine.
The creation of a user in this context is synonymous to the creation of a master
Jaseci object. These APIs are particularly useful when running a Jaseci server
or cluster in contrast to running JSCTL on the command line. Upon executing JSCTL
a dummy admin user (super\_master) is created and all state is dumped to a session
file, though any users created during a JSCTL session will indeed be created as
part of that session's state.

<div class='actionHeading'>user create</div>

 <div class='actionName'> cli: user create | api: user_create | auth: public </div> 
 <div class ='actionsArgs'> name: str (*req), password: str (), global_init: str (), global_init_ctx: dict ({}), other_fields: dict ({})</div>
 <div class ='mainbody'> <div class ='actionsDescription'>This API is used to create users and optionally set them up with a graph and
related initialization. In the context of
JSCTL, any name is sufficient and no additional information is required.
However, for Jaseci serving (whether it be the official Jaseci server, or a
custom overloaded server) additional fields are required and should be added
to the other fields parameter as per the specifics of the encapsulating server
requirements. In the case of the official Jaseci server, the name field must
be a valid email, and a password field must be passed through other fields.
A number of other optional parameters can also be passed through other feilds.
\vspace{3mm}\par
This single API call can also be used to fully set up and initialize a user
by leveraging the global init parameter. When set, this parameter attaches the
user to the global sentinel, creates a new graph for the user, sets it as the
active graph, then runs an initialization walker on the root node of this new
graph. The initialization walker is identified by the name assigned to
global init. The default empty string assigned to global init indicates this
global setup should not be run.<div class='heading'>Params</div> 
 <div class='params'> Params 
name -- The user name to create. For Jaseci server this must be a valid
email address. <br> 

global_init -- The name of an initialization walker. When set the user is
linked to the global sentinel and the walker is run on a new active graph
created for the user. <br> 

global_init_ctx -- Context to preload for the initialization walker <br> 

other_fields -- This parameter is used for additional fields required for
overloaded interfaces. This parameter is not used in JSCTL, but is used
by Jaseci server for the additional parameters of password, is_activated,
and is_superuser. <br> 
</div></div> </div> 
 
<div class='actionHeading'>user delete</div>

 <div class='actionName'> cli: user delete | api: user_delete | auth: admin </div> 
 <div class ='actionsArgs'> name: str (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>This API is used to delete a user account.<div class='heading'>Params</div> 
 <div class='params'> Params 
name -- The user name to delete. For Jaseci server this must
be a valid email address. <br> 
</div></div> </div> 
 
<div class='actionHeading'>user deleteself</div>

 <div class='actionName'> cli: user deleteself | api: user_deleteself | auth: user </div> 
 <div class ='actionsArgs'> n/a</div>
 <div class ='mainbody'> <div class ='actionsDescription'>This API is used to delete a user account.</div> </div> 
 
 # APIs for walker

The walker set of APIs are used for execution and management of walkers. Walkers
are the primary entry points for running Jac programs. The
primary API used to run walkers is \textbf{walker\_run}. There are a number of
variations on this API that enable the invocation of walkers with various
semantics.

<div class='actionHeading'>walker get</div>

 <div class='actionName'> cli: walker get | api: walker_get | auth: user </div> 
 <div class ='actionsArgs'> wlk: Walker (*req), mode: str (default), detailed: bool (False)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>Valid modes: {default, code, ir, keys, }</div> </div> 
 
<div class='actionHeading'>walker total</div>

 <div class='actionName'> cli: walker total | api: walker_total | auth: user </div> 
 <div class ='actionsArgs'> snt: Sentinel (None), detailed: bool (False)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>walker list</div>

 <div class='actionName'> cli: walker list | api: walker_list | auth: user </div> 
 <div class ='actionsArgs'> snt: Sentinel (None), detailed: bool (False)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>walker spawn create</div>

 <div class='actionName'> cli: walker spawn create | api: walker_spawn_create | auth: user </div> 
 <div class ='actionsArgs'> name: str (*req), snt: Sentinel (None)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>walker spawn list</div>

 <div class='actionName'> cli: walker spawn list | api: walker_spawn_list | auth: user </div> 
 <div class ='actionsArgs'> detailed: bool (False)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>walker spawn delete</div>

 <div class='actionName'> cli: walker spawn delete | api: walker_spawn_delete | auth: user </div> 
 <div class ='actionsArgs'> name: str (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>walker spawn clear</div>

 <div class='actionName'> cli: walker spawn clear | api: walker_spawn_clear | auth: user </div> 
 <div class ='actionsArgs'> n/a</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>walker yield list</div>

 <div class='actionName'> cli: walker yield list | api: walker_yield_list | auth: user </div> 
 <div class ='actionsArgs'> detailed: bool (False)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>walker yield delete</div>

 <div class='actionName'> cli: walker yield delete | api: walker_yield_delete | auth: user </div> 
 <div class ='actionsArgs'> name: str (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>walker yield clear</div>

 <div class='actionName'> cli: walker yield clear | api: walker_yield_clear | auth: user </div> 
 <div class ='actionsArgs'> n/a</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>walker prime</div>

 <div class='actionName'> cli: walker prime | api: walker_prime | auth: user </div> 
 <div class ='actionsArgs'> wlk: Walker (*req), nd: Node (None), ctx: dict ({}), _req_ctx: dict ({})</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>walker execute</div>

 <div class='actionName'> cli: walker execute | api: walker_execute | auth: user </div> 
 <div class ='actionsArgs'> wlk: Walker (*req), prime: Node (None), ctx: dict ({}), _req_ctx: dict ({}), profiling: bool (False)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>walker run</div>

 <div class='actionName'> cli: walker run | api: walker_run | auth: user </div> 
 <div class ='actionsArgs'> name: str (*req), nd: Node (None), ctx: dict ({}), _req_ctx: dict ({}), snt: Sentinel (None), profiling: bool (False), is_async: bool (None)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>reports results, and cleans up walker instance.</div> </div> 
 
<div class='actionHeading'>wapi</div>

 <div class='actionName'> cli: wapi | api: wapi | auth: user </div> 
 <div class ='actionsArgs'> name: str (*req), nd: Node (None), ctx: dict ({}), _req_ctx: dict ({}), snt: Sentinel (None), profiling: bool (False)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
<div class='actionHeading'>walker summon</div>

 <div class='actionName'> cli: walker summon | api: walker_summon | auth: public </div> 
 <div class ='actionsArgs'> key: str (*req), wlk: Walker (*req), nd: Node (*req), ctx: dict ({}), _req_ctx: dict ({}), global_sync: bool (True)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>along with the walker id and node id</div> </div> 
 
<div class='actionHeading'>walker callback</div>

 <div class='actionName'> cli: walker callback | api: walker_callback | auth: public </div> 
 <div class ='actionsArgs'> nd: Node (*req), wlk: Walker (*req), key: str (*req), ctx: dict ({}), _req_ctx: dict ({}), global_sync: bool (True)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>along with the walker id and node id</div> </div> 
 
 # APIs for webhook

No documentation yet.

<div class='actionHeading'>webhook</div>

 <div class='actionName'> cli: webhook | api: webhook | auth: public </div> 
 <div class ='actionsArgs'> provider: str (*req), _req_ctx: dict ({}), _raw_req_ctx: str (None)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 # APIs for apps_v1

Ref: https://openapi-generator.tech

Do not edit the class manually.

 # APIs for core_v1

Ref: https://openapi-generator.tech

Do not edit the class manually.

 # APIs for rbac_authorization_v1

Ref: https://openapi-generator.tech

Do not edit the class manually.

