<table id='cheatsheet'>  <tr> <th>Interface</th> <th>Parameters</th> </tr><tr> 
 <td>info</td><td> 
 <ul><li>n/a</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>walker summon</td><td> 
 <ul><li>key: str (*req)</li>
<li> wlk: Walker (*req)</li>
<li> nd: Node (*req)</li>
<li> ctx: dict (\{\})</li>
<li> _req_ctx: dict (\{\})</li>
<li> global_sync: bool (True)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>walker callback</td><td> 
 <ul><li>nd: Node (*req)</li>
<li> wlk: Walker (*req)</li>
<li> key: str (*req)</li>
<li> ctx: dict (\{\})</li>
<li> _req_ctx: dict (\{\})</li>
<li> global_sync: bool (True)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>walker get</td><td> 
 <ul><li>wlk: Walker (*req)</li>
<li> mode: str (default)</li>
<li> detailed: bool (False)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>walker total</td><td> 
 <ul><li>snt: Sentinel (None)</li>
<li> detailed: bool (False)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>walker list</td><td> 
 <ul><li>snt: Sentinel (None)</li>
<li> detailed: bool (False)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>walker spawn create</td><td> 
 <ul><li>name: str (*req)</li>
<li> snt: Sentinel (None)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>walker spawn list</td><td> 
 <ul><li>detailed: bool (False)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>walker spawn delete</td><td> 
 <ul><li>name: str (*req)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>walker spawn clear</td><td> 
 <ul><li>n/a</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>walker yield list</td><td> 
 <ul><li>detailed: bool (False)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>walker yield delete</td><td> 
 <ul><li>name: str (*req)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>walker yield clear</td><td> 
 <ul><li>n/a</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>walker prime</td><td> 
 <ul><li>wlk: Walker (*req)</li>
<li> nd: Node (None)</li>
<li> ctx: dict (\{\})</li>
<li> _req_ctx: dict (\{\})</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>walker execute</td><td> 
 <ul><li>wlk: Walker (*req)</li>
<li> prime: Node (None)</li>
<li> ctx: dict (\{\})</li>
<li> _req_ctx: dict (\{\})</li>
<li> profiling: bool (False)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>walker run</td><td> 
 <ul><li>name: str (*req)</li>
<li> nd: Node (None)</li>
<li> ctx: dict (\{\})</li>
<li> _req_ctx: dict (\{\})</li>
<li> snt: Sentinel (None)</li>
<li> profiling: bool (False)</li>
<li> is_async: bool (None)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>walker queue check</td><td> 
 <ul><li>task_id: str ()</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>walker queue wait</td><td> 
 <ul><li>task_id: str (*req)</li>
<li> timeout: int (30)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>user create</td><td> 
 <ul><li>name: str (*req)</li>
<li> password: str ()</li>
<li> global_init: str ()</li>
<li> global_init_ctx: dict (\{\})</li>
<li> other_fields: dict (\{\})</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>user deleteself</td><td> 
 <ul><li>n/a</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>user delete</td><td> 
 <ul><li>name: str (*req)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>webhook</td><td> 
 <ul><li>provider: str (*req)</li>
<li> _req_ctx: dict (\{\})</li>
<li> _raw_req_ctx: str (None)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>alias register</td><td> 
 <ul><li>name: str (*req)</li>
<li> value: str (*req)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>alias list</td><td> 
 <ul><li>n/a</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>alias delete</td><td> 
 <ul><li>name: str (*req)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>alias clear</td><td> 
 <ul><li>n/a</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>global get</td><td> 
 <ul><li>name: str (*req)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>global set</td><td> 
 <ul><li>name: str (*req)</li>
<li> value: str (*req)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>global delete</td><td> 
 <ul><li>name: str (*req)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>global sentinel set</td><td> 
 <ul><li>snt: Sentinel (None)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>global sentinel unset</td><td> 
 <ul><li>n/a</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>object get</td><td> 
 <ul><li>obj: Element (*req)</li>
<li> depth: int (0)</li>
<li> detailed: bool (False)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>object perms get</td><td> 
 <ul><li>obj: Element (*req)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>object perms set</td><td> 
 <ul><li>obj: Element (*req)</li>
<li> mode: str (*req)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>object perms default</td><td> 
 <ul><li>mode: str (*req)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>object perms grant</td><td> 
 <ul><li>obj: Element (*req)</li>
<li> mast: Element (*req)</li>
<li> read_only: bool (False)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>object perms revoke</td><td> 
 <ul><li>obj: Element (*req)</li>
<li> mast: Element (*req)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>graph create</td><td> 
 <ul><li>set_active: bool (True)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>graph get</td><td> 
 <ul><li>nd: Node (None)</li>
<li> mode: str (default)</li>
<li> detailed: bool (False)</li>
<li> depth: int (0)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>graph list</td><td> 
 <ul><li>detailed: bool (False)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>graph active set</td><td> 
 <ul><li>gph: Graph (*req)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>graph active unset</td><td> 
 <ul><li>n/a</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>graph active get</td><td> 
 <ul><li>detailed: bool (False)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>graph delete</td><td> 
 <ul><li>gph: Graph (*req)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>graph node get</td><td> 
 <ul><li>nd: Node (*req)</li>
<li> keys: list ([])</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>graph node view</td><td> 
 <ul><li>nd: Node (None)</li>
<li> detailed: bool (False)</li>
<li> show_edges: bool (False)</li>
<li> node_type: str ()</li>
<li> edge_type: str ()</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>graph node set</td><td> 
 <ul><li>nd: Node (*req)</li>
<li> ctx: dict (*req)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>graph walk (cli only)</td><td> 
 <ul><li>nd: Node (None)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>sentinel register</td><td> 
 <ul><li>name: str (default)</li>
<li> code: str ()</li>
<li> code_dir: str (./)</li>
<li> opt_level: int (4)</li>
<li> mode: str (default)</li>
<li> encoded: bool (False)</li>
<li> auto_run: str (init)</li>
<li> auto_run_ctx: dict (\{\})</li>
<li> auto_create_graph: bool (True)</li>
<li> set_active: bool (True)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>sentinel pull</td><td> 
 <ul><li>set_active: bool (True)</li>
<li> on_demand: bool (True)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>sentinel get</td><td> 
 <ul><li>snt: Sentinel (None)</li>
<li> mode: str (default)</li>
<li> detailed: bool (False)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>sentinel set</td><td> 
 <ul><li>code: str (*req)</li>
<li> code_dir: str (./)</li>
<li> opt_level: int (4)</li>
<li> encoded: bool (False)</li>
<li> snt: Sentinel (None)</li>
<li> mode: str (default)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>sentinel list</td><td> 
 <ul><li>detailed: bool (False)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>sentinel test</td><td> 
 <ul><li>snt: Sentinel (None)</li>
<li> single: str ()</li>
<li> detailed: bool (False)</li>
<li> profiling: bool (False)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>sentinel active set</td><td> 
 <ul><li>snt: Sentinel (*req)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>sentinel active unset</td><td> 
 <ul><li>n/a</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>sentinel active global</td><td> 
 <ul><li>auto_run: str ()</li>
<li> auto_run_ctx: dict (\{\})</li>
<li> auto_create_graph: bool (False)</li>
<li> detailed: bool (False)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>sentinel active get</td><td> 
 <ul><li>detailed: bool (False)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>sentinel delete</td><td> 
 <ul><li>snt: Sentinel (*req)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>wapi</td><td> 
 <ul><li>name: str (*req)</li>
<li> nd: Node (None)</li>
<li> ctx: dict (\{\})</li>
<li> _req_ctx: dict (\{\})</li>
<li> snt: Sentinel (None)</li>
<li> profiling: bool (False)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>architype register</td><td> 
 <ul><li>code: str (*req)</li>
<li> encoded: bool (False)</li>
<li> snt: Sentinel (None)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>architype get</td><td> 
 <ul><li>arch: Architype (*req)</li>
<li> mode: str (default)</li>
<li> detailed: bool (False)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>architype set</td><td> 
 <ul><li>arch: Architype (*req)</li>
<li> code: str (*req)</li>
<li> mode: str (default)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>architype list</td><td> 
 <ul><li>snt: Sentinel (None)</li>
<li> kind: str (None)</li>
<li> detailed: bool (False)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>architype count</td><td> 
 <ul><li>snt: Sentinel (None)</li>
<li> kind: str (None)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>architype delete</td><td> 
 <ul><li>arch: Architype (*req)</li>
<li> snt: Sentinel (None)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>master create</td><td> 
 <ul><li>name: str (*req)</li>
<li> password: str ()</li>
<li> global_init: str ()</li>
<li> global_init_ctx: dict (\{\})</li>
<li> other_fields: dict (\{\})</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>master get</td><td> 
 <ul><li>name: str (*req)</li>
<li> mode: str (default)</li>
<li> detailed: bool (False)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>master list</td><td> 
 <ul><li>detailed: bool (False)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>master active set</td><td> 
 <ul><li>name: str (*req)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>master active unset</td><td> 
 <ul><li>n/a</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>master active get</td><td> 
 <ul><li>detailed: bool (False)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>master self</td><td> 
 <ul><li>detailed: bool (False)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>master delete</td><td> 
 <ul><li>name: str (*req)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>master createsuper</td><td> 
 <ul><li>name: str (*req)</li>
<li> password: str ()</li>
<li> global_init: str ()</li>
<li> global_init_ctx: dict (\{\})</li>
<li> other_fields: dict (\{\})</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>master allusers</td><td> 
 <ul><li>limit: int (0)</li>
<li> offset: int (0)</li>
<li> asc: bool (False)</li>
<li> search: str (None)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>master become</td><td> 
 <ul><li>mast: Master (*req)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>master unbecome</td><td> 
 <ul><li>n/a</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>load yaml</td><td> 
 <ul><li>files: list (*req)</li>
<li> namespace: str (default)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>apply yaml</td><td> 
 <ul><li>name: str (*req)</li>
<li> file: list (*req)</li>
<li> unsafe_paraphrase: str ()</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>service refresh</td><td> 
 <ul><li>name: str (*req)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>service call</td><td> 
 <ul><li>svc: str (*req)</li>
<li> attrs: list ([])</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>jsorc actions load</td><td> 
 <ul><li>name: str (*req)</li>
<li> mode: str (*req)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>jsorc actions status</td><td> 
 <ul><li>name: str (*req)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>jsorc actions unload</td><td> 
 <ul><li>name: str (*req)</li>
<li> mode: str (auto)</li>
<li> retire_svc: bool (True)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>jsorc actions config</td><td> 
 <ul><li>config: str (*req)</li>
<li> name: str (*req)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>jsorc trackact start</td><td> 
 <ul><li>n/a</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>jsorc trackact stop</td><td> 
 <ul><li>n/a</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>jsorc benchmark start</td><td> 
 <ul><li>n/a</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>jsorc benchmark report</td><td> 
 <ul><li>n/a</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>jsorc benchmark stop</td><td> 
 <ul><li>report: bool (True)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>jsorc tracksys start</td><td> 
 <ul><li>n/a</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>jsorc tracksys report</td><td> 
 <ul><li>n/a</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>jsorc tracksys stop</td><td> 
 <ul><li>n/a</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>jsorc actionpolicy set</td><td> 
 <ul><li>policy_name: str (*req)</li>
<li> policy_params: dict (\{\})</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>jsorc actionpolicy get</td><td> 
 <ul><li>n/a</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>jsorc loadtest</td><td> 
 <ul><li>test: str (*req)</li>
<li> experiment: str ()</li>
<li> mem: int (0)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>config get</td><td> 
 <ul><li>name: str (*req)</li>
<li> do_check: bool (True)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>config set</td><td> 
 <ul><li>name: str (*req)</li>
<li> value: str (*req)</li>
<li> do_check: bool (True)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>config list</td><td> 
 <ul><li>n/a</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>config index</td><td> 
 <ul><li>n/a</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>config exists</td><td> 
 <ul><li>name: str (*req)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>config delete</td><td> 
 <ul><li>name: str (*req)</li>
<li> do_check: bool (True)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>logger http connect</td><td> 
 <ul><li>host: str (*req)</li>
<li> port: int (*req)</li>
<li> url: str (*req)</li>
<li> log: str (all)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>logger http clear</td><td> 
 <ul><li>log: str (all)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>logger get</td><td> 
 <ul><li>search: str ()</li>
<li> level: str (None)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>logger list</td><td> 
 <ul><li>n/a</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>actions load local</td><td> 
 <ul><li>file: str (*req)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>actions load remote</td><td> 
 <ul><li>url: str (*req)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>actions load module</td><td> 
 <ul><li>mod: str (*req)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>actions list</td><td> 
 <ul><li>name: str ()</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>actions module list</td><td> 
 <ul><li>detailed: bool (False)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>actions unload module</td><td> 
 <ul><li>name: str (*req)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>actions unload action</td><td> 
 <ul><li>name: str (*req)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>actions unload actionset</td><td> 
 <ul><li>name: str (*req)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>prometheus metrics list</td><td> 
 <ul><li>n/a</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>prometheus pod list</td><td> 
 <ul><li>namespace: str ()</li>
<li> exclude_prom: bool (False)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>prometheus pod info</td><td> 
 <ul><li>namespace: str ()</li>
<li> exclude_prom: bool (False)</li>
<li> timestamp: int (0)</li>
<li> duration: int (0)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>jac build (cli only)</td><td> 
 <ul><li>file: str (*req)</li>
<li> out: str ()</li>
<li> opt_level: int (4)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>jac disas (cli only)</td><td> 
 <ul><li>file: str (*req)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>jac test (cli only)</td><td> 
 <ul><li>file: str (*req)</li>
<li> single: str ()</li>
<li> profiling: bool (False)</li>
<li> detailed: bool (False)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>jac run (cli only)</td><td> 
 <ul><li>file: str (*req)</li>
<li> walk: str (init)</li>
<li> ctx: dict (\{\})</li>
<li> profiling: bool (False)</li>
</ul> 
 </td> 
 </tr><tr> 
 <td>jac dot (cli only)</td><td> 
 <ul><li>file: str (*req)</li>
<li> walk: str (init)</li>
<li> ctx: dict (\{\})</li>
<li> detailed: bool (False)</li>
</ul> 
 </td> 
 </tr></table>