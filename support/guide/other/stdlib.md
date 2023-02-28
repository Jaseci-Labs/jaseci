
# date

No documentation yet.
 <div class='actionName'> date.quantize_to_year </div> 
 <div class ='actionsArgs'> date: str (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> date.quantize_to_month </div> 
 <div class ='actionsArgs'> date: str (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> date.quantize_to_week </div> 
 <div class ='actionsArgs'> date: str (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> date.quantize_to_day </div> 
 <div class ='actionsArgs'> date: str (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> date.datetime_now </div> 
 <div class ='actionsArgs'> n/a</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> date.date_now </div> 
 <div class ='actionsArgs'> n/a</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> date.timestamp_now </div> 
 <div class ='actionsArgs'> n/a</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> date.date_day_diff </div> 
 <div class ='actionsArgs'> start_date: str (*req), end_date: str (None)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 

# elastic

No documentation yet.
 <div class='actionName'> elastic.post </div> 
 <div class ='actionsArgs'> url: str (*req), body: dict (*req), index: str (), suffix: str ()</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> elastic.post_act </div> 
 <div class ='actionsArgs'> url: str (*req), body: dict (*req), suffix: str ()</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> elastic.get </div> 
 <div class ='actionsArgs'> url: str (*req), body: dict (*req), index: str (), suffix: str ()</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> elastic.get_act </div> 
 <div class ='actionsArgs'> url: str (*req), body: dict (*req), suffix: str ()</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> elastic.doc </div> 
 <div class ='actionsArgs'> log: dict (*req), query: str (), index: str (), suffix: str ()</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> elastic.doc_activity </div> 
 <div class ='actionsArgs'> log: dict (*req), query: str (), suffix: str ()</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> elastic.search </div> 
 <div class ='actionsArgs'> body: dict (*req), query: str (), index: str (), suffix: str ()</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> elastic.search_activity </div> 
 <div class ='actionsArgs'> body: dict (*req), query: str (), suffix: str ()</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> elastic.mapping </div> 
 <div class ='actionsArgs'> query: str (), index: str (), suffix: str ()</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> elastic.mapping_activity </div> 
 <div class ='actionsArgs'> query: str (), suffix: str ()</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> elastic.aliases </div> 
 <div class ='actionsArgs'> query: str (pretty=true)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> elastic.reindex </div> 
 <div class ='actionsArgs'> body: dict (*req), query: str (pretty)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 

# file

No documentation yet.
 <div class='actionName'> file.load_str </div> 
 <div class ='actionsArgs'> fn: str (*req), max_chars: int (None)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> file.load_json </div> 
 <div class ='actionsArgs'> fn: str (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> file.load_to_b64 </div> 
 <div class ='actionsArgs'> fn: str (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> file.dump_str </div> 
 <div class ='actionsArgs'> fn: str (*req), s: str (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> file.dump_json </div> 
 <div class ='actionsArgs'> fn: str (*req), obj: _empty (*req), indent: int (None)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> file.dump_from_b64 </div> 
 <div class ='actionsArgs'> fn: str (*req), b64: str (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> file.append_str </div> 
 <div class ='actionsArgs'> fn: str (*req), s: str (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> file.append_from_b64 </div> 
 <div class ='actionsArgs'> fn: str (*req), b64: str (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> file.delete </div> 
 <div class ='actionsArgs'> fn: str (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 

# internal

No documentation yet.
 <div class='actionName'> internal.start_perf_test </div> 
 <div class ='actionsArgs'> name: str (default)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> internal.stop_perf_test </div> 
 <div class ='actionsArgs'> name: str (default)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 

# mail

No documentation yet.
 <div class='actionName'> mail.send </div> 
 <div class ='actionsArgs'> sender: _empty (*req), recipients: _empty (*req), subject: _empty (*req), text: _empty (*req), html: _empty (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 

# net

This library of actions cover the standard operations that can be
run on graph elements (nodes and edges). A number of these actions
accept lists that are exclusively composed of instances of defined
architype node and/or edges. Keep in mind that a \lstinline{jac_set}
is simply a list that only contains such elements.
 <div class='actionName'> net.max </div> 
 <div class ='actionsArgs'> item_set: JacSet (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>This action will return the maximum element in a list of nodes
and/or edges based on an anchor has variable. Since each node or edge can only
specify a single anchor this action enables a handy short hand for utilizing the
anchor variable as the representative field for performing the  comparison in
ranking. This action does not support arhcitypes lacking an anchor.
\par
For example, if you have a node called \lstinline{movie review} with a
field \lstinline{has anchor score = .5;} that changes based on sentiment
analysis, using this action will return the node with the highest score from the
input list of nodes.<div class='heading'>Params</div> 
 <div class='params'> Params 
item_set -- A list of node and or edges to identify the
maximum element based on their respective anchor values <br> 
</div><div class='heading'>Returns</div> 
<div class='return'>Returns - A node or edge object</div> </div> 
 
 <div class='actionName'> net.min </div> 
 <div class ='actionsArgs'> item_set: JacSet (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>This action will return the minimum element in a list of nodes
and/or edges. This action exclusively utilizes the anchor variable
of the node/edge arhcitype as the representative field for
performing the comparison in ranking. This action does not support
arhcitypes lacking an anchor. (see action max for an example)<div class='heading'>Params</div> 
 <div class='params'> Params 
item_set -- A list of node and or edges to identify the
minimum element based on their respective anchor values <br> 
</div><div class='heading'>Returns</div> 
<div class='return'>Returns - A node or edge object</div> </div> 
 
 <div class='actionName'> net.pack </div> 
 <div class ='actionsArgs'> item_set: JacSet (*req), destroy: bool (False)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>This action takes a subgraph as a collection of nodes in a list and
creates a generic dictionary representation of the subgraph inclusive of
all edges between nodes inside the collection. Note that any edges that are
connecting nodes outside of the list of nodes are omitted from the packed
subgraph representation. The complete context of all nodes and connecting edges
are retained in the packed dictionary format. The unpack action can then be used
to instantiate the identical subgraph back into a graph. Packed graphs are
highly portable and can be used for many use cases such as exporting graphs and
subgraphs to be imported using the unpack action.<div class='heading'>Params</div> 
 <div class='params'> Params 
item_set -- A list of nodes comprising the subgraph to be packed. Edges can be
included in this list but is ultimately ignored. All edges from the actual nodes
in the context of the source graph will be automatically included in the packed
dictionary if it contects two nodes within this input list. <br> 

destroy -- A flag indicating whether the original graph nodes covered by pack
operation should be destroyed. <br> 
</div><div class='heading'>Returns</div> 
<div class='return'>Returns - A generic and portable dictionary representation of the subgraph</div> </div> 
 
 <div class='actionName'> net.unpack </div> 
 <div class ='actionsArgs'> graph_dict: dict (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>This action takes a dictionary in the format produced by the packed action
to instantiate a set of nodes and edges corresponding to the subgraph represented
by the pack action. The original contexts that were pack will also be created.
Important Note: When using this unpack action, the unpacked collections of elements
returned must be connected to a source graph to avoid memory leaks.<div class='heading'>Params</div> 
 <div class='params'> Params 
graph_dict -- A dictionary in the format produced by the pack action. <br> 
</div><div class='heading'>Returns</div> 
<div class='return'>Returns - A list of the nodes and edges that were created corresponding to the
input packed format. Note: Must be then connected to a source graph to avoid memory
leak.</div> </div> 
 
 <div class='actionName'> net.root </div> 
 <div class ='actionsArgs'> n/a</div>
 <div class ='mainbody'> <div class ='actionsDescription'>This action returns the root node for the graph of a given user (master). A call
to this action is only valid if the user has an active graph set, otherwise it
return null. This is a handy way for any walker to get to the root node of a
graph from anywhere.<div class='heading'>Returns</div> 
<div class='return'>Returns - The root node of the active graph for a user. If none set, returns null.</div> </div> 
 

# rand

No documentation yet.
 <div class='actionName'> rand.seed </div> 
 <div class ='actionsArgs'> val: int (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> rand.integer </div> 
 <div class ='actionsArgs'> start: int (*req), end: int (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> rand.choice </div> 
 <div class ='actionsArgs'> lst: list (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> rand.uniform </div> 
 <div class ='actionsArgs'> low: float (*req), high: float (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> rand.sentence </div> 
 <div class ='actionsArgs'> min_lenth: int (4), max_length: int (10), sep: str ( )</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> rand.paragraph </div> 
 <div class ='actionsArgs'> min_lenth: int (4), max_length: int (8), sep: str ( )</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> rand.text </div> 
 <div class ='actionsArgs'> min_lenth: int (3), max_length: int (6), sep: str (nn)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> rand.word </div> 
 <div class ='actionsArgs'> n/a</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> rand.time </div> 
 <div class ='actionsArgs'> start_date: str (*req), end_date: str (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 

# request

No documentation yet.
 <div class='actionName'> request.get </div> 
 <div class ='actionsArgs'> url: str (*req), data: dict (*req), header: dict (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>Param 1 - url
Param 2 - data
Param 3 - header

Return - response object</div> </div> 
 
 <div class='actionName'> request.post </div> 
 <div class ='actionsArgs'> url: str (*req), data: dict (*req), header: dict (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>Param 1 - url
Param 2 - data
Param 3 - header

Return - response object</div> </div> 
 
 <div class='actionName'> request.put </div> 
 <div class ='actionsArgs'> url: str (*req), data: dict (*req), header: dict (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>Param 1 - url
Param 2 - data
Param 3 - header

Return - response object</div> </div> 
 
 <div class='actionName'> request.delete </div> 
 <div class ='actionsArgs'> url: str (*req), data: dict (*req), header: dict (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>Param 1 - url
Param 2 - data
Param 3 - header

Return - response object</div> </div> 
 
 <div class='actionName'> request.head </div> 
 <div class ='actionsArgs'> url: str (*req), data: dict (*req), header: dict (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>Param 1 - url
Param 2 - data
Param 3 - header

Return - response object</div> </div> 
 
 <div class='actionName'> request.options </div> 
 <div class ='actionsArgs'> url: str (*req), data: dict (*req), header: dict (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>Param 1 - url
Param 2 - data
Param 3 - header

Return - response object</div> </div> 
 
 <div class='actionName'> request.multipart_base64 </div> 
 <div class ='actionsArgs'> url: str (*req), files: list (*req), header: dict (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>Param 1 - url
Param 3 - header
Param 3 - file (Optional) used for single file
Param 4 - files (Optional) used for multiple files
Note - file and files can't be None at the same time

Return - response object</div> </div> 
 
 <div class='actionName'> request.file_download_base64 </div> 
 <div class ='actionsArgs'> url: str (*req), header: dict (*req), encoding: str (utf-8)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 

# std

No documentation yet.
 <div class='actionName'> std.log </div> 
 <div class ='actionsArgs'> args: _empty (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> std.out </div> 
 <div class ='actionsArgs'> args: _empty (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> std.js_input </div> 
 <div class ='actionsArgs'> prompt: str ()</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> std.js_round </div> 
 <div class ='actionsArgs'> num: float (*req), digits: int (0)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> std.err </div> 
 <div class ='actionsArgs'> args: _empty (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> std.sort_by_col </div> 
 <div class ='actionsArgs'> lst: list (*req), col_num: int (*req), reverse: bool (False)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>Param 1 - list
Param 2 - col number
Param 3 - boolean as to whether things should be reversed

Return - Sorted list</div> </div> 
 
 <div class='actionName'> std.time_now </div> 
 <div class ='actionsArgs'> n/a</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> std.set_global </div> 
 <div class ='actionsArgs'> name: str (*req), value: _empty (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>Param 1 - name
Param 2 - value (must be json serializable)</div> </div> 
 
 <div class='actionName'> std.get_global </div> 
 <div class ='actionsArgs'> name: str (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>Param 1 - name</div> </div> 
 
 <div class='actionName'> std.actload_local </div> 
 <div class ='actionsArgs'> filename: str (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> std.actload_remote </div> 
 <div class ='actionsArgs'> url: str (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> std.actload_module </div> 
 <div class ='actionsArgs'> module: str (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> std.destroy_global </div> 
 <div class ='actionsArgs'> name: str (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> std.set_perms </div> 
 <div class ='actionsArgs'> obj: Element (*req), mode: str (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>Param 1 - target element
Param 2 - valid permission (public, private, read only)

Return - true/false whether successful</div> </div> 
 
 <div class='actionName'> std.get_perms </div> 
 <div class ='actionsArgs'> obj: Element (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>Param 1 - target element

Return - Sorted list</div> </div> 
 
 <div class='actionName'> std.grant_perms </div> 
 <div class ='actionsArgs'> obj: Element (*req), mast: Element (*req), read_only: bool (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>Param 1 - target element
Param 2 - master to be granted permission
Param 3 - Boolean read only flag

Return - Sorted list</div> </div> 
 
 <div class='actionName'> std.revoke_perms </div> 
 <div class ='actionsArgs'> obj: Element (*req), mast: Element (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>Param 1 - target element
Param 2 - master to be revoked permission

Return - Sorted list</div> </div> 
 
 <div class='actionName'> std.get_report </div> 
 <div class ='actionsArgs'> n/a</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> std.clear_report </div> 
 <div class ='actionsArgs'> n/a</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> std.log_activity </div> 
 <div class ='actionsArgs'> log: dict (*req), action: str (), query: str (), suffix: str ()</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 

# stripe

No documentation yet.
 <div class='actionName'> stripe.create_product </div> 
 <div class ='actionsArgs'> name: str (*req), description: str (*req), kwargs: _empty (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> stripe.create_product_price </div> 
 <div class ='actionsArgs'> productId: str (*req), amount: int (*req), currency: str (*req), recurring: dict ({}), kwargs: _empty (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> stripe.product_list </div> 
 <div class ='actionsArgs'> detailed: bool (False), kwargs: _empty (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> stripe.create_customer </div> 
 <div class ='actionsArgs'> email: str (*req), name: str (*req), address: dict ({}), kwargs: _empty (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> stripe.get_customer </div> 
 <div class ='actionsArgs'> customer_id: str (*req), kwargs: _empty (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> stripe.attach_payment_method </div> 
 <div class ='actionsArgs'> payment_method_id: str (*req), customer_id: str (*req), kwargs: _empty (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> stripe.detach_payment_method </div> 
 <div class ='actionsArgs'> payment_method_id: str (*req), kwargs: _empty (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> stripe.get_payment_methods </div> 
 <div class ='actionsArgs'> customer_id: str (*req), kwargs: _empty (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> stripe.update_default_payment_method </div> 
 <div class ='actionsArgs'> customer_id: str (*req), payment_method_id: str (*req), kwargs: _empty (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> stripe.create_invoice </div> 
 <div class ='actionsArgs'> customer_id: str (*req), kwargs: _empty (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> stripe.get_invoice_list </div> 
 <div class ='actionsArgs'> customer_id: str (*req), subscription_id: str (*req), starting_after: str (), limit: int (10), kwargs: _empty (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> stripe.get_payment_intents </div> 
 <div class ='actionsArgs'> customer_id: str (*req), starting_after: str (), limit: int (10), kwargs: _empty (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> stripe.create_payment_intents </div> 
 <div class ='actionsArgs'> customer_id: str (*req), amount: int (*req), currency: str (*req), payment_method_types: list (['card']), kwargs: _empty (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> stripe.get_customer_subscription </div> 
 <div class ='actionsArgs'> customer_id: str (*req), kwargs: _empty (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> stripe.create_payment_method </div> 
 <div class ='actionsArgs'> card_type: str (*req), card: dict (*req), billing_details: dict (*req), kwargs: _empty (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> stripe.create_trial_subscription </div> 
 <div class ='actionsArgs'> customer_id: str (*req), items: list (*req), payment_method_id: str (), trial_period_days: int (14), kwargs: _empty (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> stripe.create_subscription </div> 
 <div class ='actionsArgs'> customer_id: str (*req), items: list (*req), payment_method_id: str (), kwargs: _empty (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> stripe.cancel_subscription </div> 
 <div class ='actionsArgs'> subscription_id: str (*req), kwargs: _empty (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> stripe.get_subscription </div> 
 <div class ='actionsArgs'> subscription_id: str (*req), kwargs: _empty (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> stripe.update_subscription_item </div> 
 <div class ='actionsArgs'> subscription_id: str (*req), subscription_item_id: str (*req), price_id: str (*req), kwargs: _empty (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> stripe.get_invoice </div> 
 <div class ='actionsArgs'> invoice_id: str (*req), kwargs: _empty (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> stripe.create_usage_report </div> 
 <div class ='actionsArgs'> subscription_item_id: str (*req), quantity: int (*req), kwargs: _empty (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> stripe.create_checkout_session </div> 
 <div class ='actionsArgs'> success_url: str (*req), cancel_url: str (*req), line_items: list (*req), mode: str (*req), kwargs: _empty (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 
 <div class='actionName'> stripe.exec </div> 
 <div class ='actionsArgs'> api: str (*req), args: _empty (*req), kwargs: _empty (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 

# task

No documentation yet.
 <div class='actionName'> task.get_result </div> 
 <div class ='actionsArgs'> task_id: _empty (*req), wait: _empty (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 

# url

No documentation yet.
 <div class='actionName'> url.is_valid </div> 
 <div class ='actionsArgs'> url: str ()</div>
 <div class ='mainbody'> <div class ='actionsDescription'>Param 1 - url string

Return - True if valid, False if not</div> </div> 
 
 <div class='actionName'> url.ping </div> 
 <div class ='actionsArgs'> url: str ()</div>
 <div class ='mainbody'> <div class ='actionsDescription'>Param 1 - url string

Return - True if error code is in 200s, False if not</div> </div> 
 
 <div class='actionName'> url.download_text </div> 
 <div class ='actionsArgs'> url: str ()</div>
 <div class ='mainbody'> <div class ='actionsDescription'>Param 1 - url string

Return - string containing html</div> </div> 
 
 <div class='actionName'> url.download_b64 </div> 
 <div class ='actionsArgs'> url: str ()</div>
 <div class ='mainbody'> <div class ='actionsDescription'>Param 1 - url string

Return - base64 string representing the get response</div> </div> 
 

# vector

No documentation yet.
 <div class='actionName'> vector.cosine_sim </div> 
 <div class ='actionsArgs'> vec_a: list (*req), vec_b: list (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>Param 1 - First vector
Param 2 - Second vector

Return - float between 0 and 1</div> </div> 
 
 <div class='actionName'> vector.dot_product </div> 
 <div class ='actionsArgs'> vec_a: list (*req), vec_b: list (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>Param 1 - First vector
Param 2 - Second vector

Return - float between 0 and 1</div> </div> 
 
 <div class='actionName'> vector.get_centroid </div> 
 <div class ='actionsArgs'> vec_list: list (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>Param 1 - List of vectors

Return - (centroid vector, cluster tightness)</div> </div> 
 
 <div class='actionName'> vector.softmax </div> 
 <div class ='actionsArgs'> vec_list: list (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>Param 1 - List of vectors

Return - (centroid vector, cluster tightness)</div> </div> 
 
 <div class='actionName'> vector.sort_by_key </div> 
 <div class ='actionsArgs'> data: dict (*req), reverse: _empty (False), key_pos: _empty (None)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>Param 1 - List of items
Param 2 - if Reverse
Param 3 (Optional) - Index of the key to be used for sorting
if param 1 is a list of tuples.

Deprecated</div> </div> 
 
 <div class='actionName'> vector.dim_reduce_fit </div> 
 <div class ='actionsArgs'> data: list (*req), dim: _empty (2)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>Param 1 - List of vectors
Param 2 - Dimension to reduce to

Return - base64 encoded string of the model</div> </div> 
 
 <div class='actionName'> vector.dim_reduce_apply </div> 
 <div class ='actionsArgs'> data: list (*req), model: str (*req)</div>
 <div class ='mainbody'> <div class ='actionsDescription'>Param 1 - List of vectors
Param 2 - base64 encoded string of the model

Return - List of reduced vectors</div> </div> 
 

# webtool

No documentation yet.
 <div class='actionName'> webtool.get_page_meta </div> 
 <div class ='actionsArgs'> url: str ()</div>
 <div class ='mainbody'> <div class ='actionsDescription'>No documentation yet.</div> </div> 
 

# zlib

No documentation yet.
 <div class='actionName'> zlib.compress </div> 
 <div class ='actionsArgs'> data_b64: str ()</div>
 <div class ='mainbody'> <div class ='actionsDescription'>Param 1 - data in base64

Return - compressed data in base64</div> </div> 
 
 <div class='actionName'> zlib.decompress </div> 
 <div class ='actionsArgs'> data_b64: str ()</div>
 <div class ='mainbody'> <div class ='actionsDescription'>Param 1 - data in base64

Return - decompressed data in base64</div> </div> 
 
