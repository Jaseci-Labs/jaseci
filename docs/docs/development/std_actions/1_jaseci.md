# Jaseci Basic Actions Library

## Alias
Alias provides names  for long string like UUIDs.

### Register

`name` :  (`str`) - The name for the alias created by caller.
`value` : (`str`) - The value for that name to map to (i.e., UUID)

```jac
response  = jaseci.alias_register(name,value);
```

### List

List all string to string alias that caller can use

```jac
jaseci.alias_list()
```

### Delete

Delete an active string to string alias mapping

`name`: (str) - The name for the alias to be removed from caller.

```jac
jaseci.alias_delete()
```

### Clear

Removes  all aliases.

```jac
jaseci.alias_clear()
```


## Objects

### Get global Variable

`name`:(`str`) - name of global variable.

```jac
value = jaseci.global_get(name);
```

### Object Details

Return detail of jaseci object.

`object` : element - jaseci object

```jac
details = jaseci.object_get(object);
```

### Object Access Mode

Get the object access mode for any jaseci object.

`object` : element - jaseci object

```jac
accessMode  = jaseci.object_perms_set(object);
```

### Set Object access mode

`valid perms` = ["public", "private", "read_only"]
`object` : element - jaseci object
`perm`: string

```jac
jaseci.object_perms_set(element,perm);
```

### Object access grant

Grants one object the acess to another object.

`object` : element - object to access
`master` : element  - object to gain access

```jac
rent = jaseci.object_perms_grant(element, master);
```

### Revoke object access

Remove permissions for user to access a Jaseci object

`object` : element - object that was  accessed.
`master` : element  - object that has access.

```jac
ret = jaseci.object_perms_revoke(element,master);
```
## Graphs

### Create Graph

Create a graph instance and return root node graph object.

```jac
jaseci.graph_create()
```

### Get Graph Content

Return the content of the graph with mode.
Valid modes: {default, dot, }.

`gph` :graph - graph whose conten you need.
`mode` : string - "deafult" or "dot" , "default" by default.

```jac
Contents = jaseci.graph_get(gph);
```

### List Graph Objects
Provide complete list of all graph objects (list of root node objects).

`detailed` : `boolean` - if eac graph details are wanted.

```jac
graph_info = jaseci.graph_list(detailed);
```

### Set Default Graph

Set the default graph master should use.

`gph` : `graph` - graph to be default.

```jac
message = jaseci.graph_active_set(gph);
```

### Remove Default Graph

Unsets the default sentinel master should use.

```jac
jaseci.graph_active_unset();
```

### Get Default Graph

`detailed` : `boolean` - default false , true to return graph details (optional)

```jac
grph = jaseci.graph_active_get();
```
### Delete Graph

Permantely  delete graph

`grph` : `graph` - Graph to be deleted.

```jac
message = jaseci.graph_delete(grph);
```

### Return Node Value

Returns value of a given node.

`nd` : `node` - node whose value will be returned.

```jac
node_value =  jaseci.graph_node_get(nd);
```

### Set Node Value

Assigns values to member variables of a given node using ctx object.

`nd` : `node` : node to who a value will be assigned.
`ctx` : `dictionary` - values to assign.

```jac
node_details = jaseci.graph_node_set(nd,ctx);
```

## Sentinels

### Register Sentinel

Create blank or code loaded sentinel and return object.


`name`: `str` -  "default" when not specified.
`encoded`: `bool`
`auto_run`: Auto_run is the walker to execute on register (assumes active graph is selected), default is "init"
`ctx` : `dict` = {},
`set_active`: `bool` = True

```jac
sentel = jaseci.sentinel_regsiter(name,encoded,auto_run,ctx,set_active);
```

### Global Sentinel

Copies global sentinel to local master.

`set_active` : `boolean` - set sentinel to be active.
`on_demand` : `boolean` -

```jac
sentl = jaseci.sentinel_pull(set_active);
```


### Get Sentinel

Get a sentinel rendered with specific mode.

Valid modes: {default, code, ir, }
`snt` : `sentinel` : sentinel to be rendered in specific mode.
`mode` : `str` - mode sentinel will be in

```jac
snt  = jaseci.sentinel_get(snt,mode);
```

### Set Sentinel Code

Set code/ir for a sentinel, only replaces walkers/archs in sentinel.
Needs more clarity

```jac
jaseci.sentinel_set();
```

### Sentinel List

Provides Completed list of all sentinel objects

```jac
snt_list = jaseci.sentinel_list();
```

### Sentinel Test

Run battery of test cases within sentinel and provide result

`snt` : `sentinel` - sentinel to be tested

```jac
snt_details = jaseci.sentinel_test(snt);
```
### Default Sentinel

Sets the default sentinel master should use.

`snt` :`sentinel` - sentinel to be made default

```jac
message = jaseci.sentinel_active_set(snt);
```

### Remove Default Sentinel

Unsets the default sentinel master should use.

```jac
messsage = jaseci.sentinel_active_unset();
```

### Set Global Sentinel

Sets the default master sentinel to the global sentinel.

```jac
response  = jaseci.sentinel_active_global();
```
### Return default Sentinel

Returns the default sentinel master is using
```jac
response = jaseci.sentinel_active_get();
```

### Delete Sentinel

Permanently delete sentinel with given id.

`snt` : `sentinel` - sentinel to be deleted

```jac
message = jaseci.sentinel_delete(snt);
```

## Walker

### Run Walker

Clarity needed
Run a walker on a specific node
`wlk` : `walker` - walker to be ran
`nd` : `node` -  node where walker will be placed
`ctx` : `dictionary`  - context for walker

```jac
response  = jaseci.walker_summon();
```

### Register Walker

Clarity needed.
Create blank or code loaded walker and return object.

```jac
walker_seralized = jaseci.walker_register();
```
### Get Walker

Get a walker rendered with specific mode.
`wlk` : `walker` - walker to be rendered.
`mode` : `str` - mode to return walker.

Valid modes: {default, code, ir, keys, }

```jac
wlk_response = jaseci.walker_get(wlk,mode);
```
### Set Walker code

Set code/ir for a walker.
Valid modes: {code, ir, }
`wlk` :`walker` - walker code/ir to be set
`code` : `str` - "code" or  "ir"

```jac
message = jaseci..walker_set(wlk,code);
```

### List Walkers

List walkers known to sentinel.
`snt` :`sentinel` - active sentinel

```jac
walkers = jaseci.walker_list();
```
### Delete Walker

Permantely delete walker with given id
`wlk` : `walker` - walker to be deleted
`snt` : `sentinel` - sentinel where walker resides

```jac
message = jaseci.walker_delete(wlk,snt);
```

### Spawn Walker

Creates new instance of walker and returns new walker object.
`name` : `str` - name of walker
`snt` : `sentinel` - sentinel the walker will be under

```jac
spawn_wlk = jaseci.walker_spawn_create(name,snt);
```

### Delete spawned Walker

Delete instance of walker

`name` : `string` - name of walker to be deleted

```jac
jaseci.walker_spawn_delete(name);
```

### List Spawned walker

List walkers spawned by master
`detailed` : `boolean` - return details of walkers

```jac
walkers  = jaseci.walker_spawn_list(deatailed);
```

### Assign walker to node

Assigns walker to a graph node and primes walker for execution

`wlk` : `walker`  - walker to be assigned
`nd` : `node` - node walker will be assigned too
`ctx` : `dicionary`  - context for node

```jac
message   = jaseci.walker_prime(wlk,nd,ctx);
```

### Execute Walker

Execute walker assuming it is primed.
`wlk` : `walker` -  walker to execute
`nd` : `node` - node where execution will begin

```jac
response  = jaseci.walker_execute(wlk,nd);
```

### Walker run

Creates walker instance, primes walker on node, executes walker, reports results, and cleans up walker instance.

`name` : `str` - name of the walker
`nd` : `node` = Node walker will be primed on
`ctx` : `dict` -  {} by default
`snt` : `sentinel` - None  by default
`profiling` : `bool` - False by default

```jac
response =  jaseci.walker_run(name,nd,ctx,snt,profiling);
```

### Walker Individual APIs

`name` : `string` - name of walker
`nd` : `node` - node walker will be primed on
`ctx` : `dictionary` - dictionary for context information
`snt` : `sentinel` , none by default
`profiling` : `boolean` , false by default

```jac
response = jaseci.wapi(name,nd,ctx);
```

## Architypes

### Create Architype

`code` : `string` : the test or filename  for an architype jac code
`encoded` : `boolean` : if code is encoded or not
`snt (uuid)` : the uuid of the sentinel to be the owner of this architype

```jac
architype_response  = jaseci.architype_register(code,encoded,snt);
```

### Get Architype

Get an architype rendered with specific mode.

`arch` : `architype` - the architype being accessed
`mode` : `string` - valid modes {default, code, ir}
`detailed` : `boolean` - return detailed info also

```jac
architpe_serialized   = jaseci.architype_get(arch,mode,detailed);
```

### Set Architype code or ir

`arch (uuid)` : The architype being set
`code (str)` : The text (or filename) for an architypes Jac code/ir
`mode (str)` : Valid modes: {default, code, ir, }

```jac
response  = jaseci.architype_set(arch,code,mode);
```
### List Architype

List architypes know to sentinel
`snt (uuid)` : The sentinel for which to list its architypes
`detailed (bool)` : Flag to give summary or complete set of fields

```jac
archs = jaseci.architype_list(snt,detailled);
```

### Delete Architype

Permanently delete sentinel with given id.
`arch (uuid)` : The architype being set.
`snt (uuid)` : The sentinel for which to list its architypes

```jac
response = jaseci.architype_delete(arch,snt);
```


## Masters

### Create Master

Create a master instance and retrun root node master object.

`name`  : `str` - name of master
`active` : `boolean`
`ctx` : `dictionary` - additional feilds for overloaded interfaces

```jac
master_object  = jaseci.master_create(name,active,ctx);
```

### Get Master Content

Return the content of the master with mode.
`name` : `string` - name of master to be returned.
`mode` : `string` - modes{'default',}

```jac
master_object = jaseci.master_get(name,mode);
```

### List Masters

Provide complete list of all master objects (list of root node objects)
`detailed` : `boolean` - detailed info wanted.

```jac
masters  = jaseci.master_list(detailed);
```

### Set Default Master

Sets the default sentinel  master should use.

`name`  : `name` of master to be set

```jac
response  = jaseci.master_active_set(name);
```

### Unset Default Master

Unsets the default sentinel mastershould use.

```jac
response  = jaseci.master_active_unset();
```

### Get Default Master

Returns the default master master is using

`detailed` : `boolean`  - return detailed information on the master

```jac
master_serialized = jaseci.master_active_get(detailed);
```
### Get Master Object

Returns the masters object.

```jac
master_object = jaseci.master_self();
```
### Delete Master

`name` : `str` - master to be deleted

```jac
response   = jaseci.master_delete(name);
```

## Logger

APIs for Jaseci Logging configuration

### Connect to internal logger

Connects internal logging to http(s) (log msgs sent via POSTs)
Valid log params: {sys, app, all }
`host` : `string`  -
`port` : `string` -
`url` : `string` -
`log` : `string`  -

```jac
response = jaseci.logger_http_connect(host,port,url,log);
```
### Remove HTTP Handler

`log`  : `string` - default ,all

```jac
response  = jaseci.logger_http_clear(log);
```
### Check Active logger

List active loggers
```jac
response = jaseci.logger_list();
```

## Global API

### Set Global

Set a global variable
`name`  : `string` - name of global
`value` : `string` -  value of global

```jac
response = jaseci.global_set(name,value);
```
### Delete Global

Delete a global
`name` : `string` - delete globals

```jac
response = jaseci.global_delete(name);
```
### Set Global Sentinel
```jac
response = jaseci.global_sentinel_set(snt);
```
### Unset Global Sentinel

Unset globally accessible variable.
`snt` : `sentinel` - sentinel to be removed as globally acccessible.

```jac
response  = jaseci.sentinel_unset(snt);
```

## Super Master

### Super Instance of Master

Create a super instance and return root node super object
`name` : `string` - name of master
`set_active` : `boolean` - set master to active
`other_fields` : `dictionary` - used for additional feilds for overloaded interfaces (i.e., Dango interface)

```jac
master_object  = jaseci.master_createsuper(name,set_active,other_fields);
```

### Masters info

Returns info on a set of users.
`num` : `int` -  specifies the number of users to return.
`start_idx` : `int` -  specfies where to start.

```jac
# in development
```

### Set Default Master

Sets the default master master should use
`mast` : `master` - master to be used

```jac
response  = jaseci.master_become(mast);
```

### Unset  default Master

Unsets the default master master should use.

```jac
response = jaseci.master_become();
```

## Stripe

Set of APIs to expose Stripe Management

### Create Product

`name` : `string` - default "VIP Plan".
`description` : `string` - default " Plan description"

```jac
message = jaseci.stripe_product_create(name,desciption);
```

### Modify Product Price

`productId` : `string` - id of product to be modified
`amount` : `float` - amount for product ,default is 50
`interval` : `string` - default  "month"

```jac
message = jaseci.stripe_product_price_set(productId,amount,interval);
```

### List Products

Retrieve all products.
`detailed` : `boolean` - details of all products.

```jac
product_list = jaseci.stripe_product_list();
```

### Create Customer

`paymentId` : `string` - id of payment method
`name`: `string` - name of customer
`email` : `string` - email of customer
`description` : `string`  - description of customer

```jac
message =  jaseci.stripe_customer_create(paymentId,name,email,description);
```
### Get Customer Information

Retrieve customer information
CustomerId : string - id to identify customer

```jac
message = jaseci.stripe_customer_get(customerId);
```

### Add Customer Payment Method

`PaymentMethodId` : `string` - id of payment method
`customerId`  : `string` - id to uniquely identify customer

```jac
message = jaseci.stripe_customer_payment_add(paymentId,customerId);
```

### Remove Customer Payment method

`paymentMethodId` : `string` - id of payment method

```jac
message = jaseci.stripe_customer_payment_delete(paymentId);
```

### Customer's List of payment Method

Get list of customer payment method
`customerId` : `string` - id to uniquely identify customer

```jac
payment_methods = jaseci.stripe_customer_payment_get(customerId);
```
### Update Customer default payment

`paymentMethodId` : `string` - id of payment method
`customerId`  : `string` - id to uniquely identify customer

```jac
message = jaseci.stripe_customer_payment_default(customeId,paymentMethodId);
```

### Create Customer Subscription

Create customer subscription
`paymentId` : `string` - id pf payment method
`priceId` : `string` - id for price
`customerId` : `string` - id to uniquely identify customer

```jac
message = jaseci.stripe_subscription_create(paymentId,priceId,customerId);
```

### Cancel Customer Subscription

`subscriptionId` : `string` - id to uniquley identify subscription

```jac
message  = jaseci.stripe_subscription_delete(subscriptionId);
```

### Get Customer Subscription

Retrieve customer subscription.
`customerId` : `string` - id to uniquely identify customer.

```jac
customer_subscription = jaseci.stripe_subscription_get(customerId);
```

### Invoice List

Retrieve customer list of invoices.
`customerId` : `string` - id to uniquely identify customer`.
`subscriptionId` : `string` - id to uniquley identify subscription.
`limit` : `int` - max amount of invoices to return.
`lastitem` : `string` - id of item from where the return should start default is " ".

```jac
invoices = jaseci.stripe_invoice_list(customerId,subscriptionId,limit,lastitem);
```

## actions

## Load actions module locally

Hot load a python module and assimlate any jaseci action
`file` : `string` - module to be loaded

```jac
success_message  = jaseci.actions_load_local(file);
```

### Load actions module remote

Hot load an actions set from live pod at URL
`url` : `string` - link to module to be loaded

```jac
success_message = jaseci.actions_load_remote(url);
```
### Load actions module local

`mod` : `string` - name of module to be loaded

```jac
success_messsage = jaseci,actions_load_module(mod);
```

### List actions

```jac
actions = jaseci.actions_list();
```

## Configurations APIs

### Get config

Get a Connfig
`name` : `string` - name of configurations.
`do_check` : `boolean` - deafult is True

```jac
confid_details = jaseci.config_get(name,do_check);
```

###  Set Config

`name` : `string` - name of configuration
`value` : `string` - value to set
`do_check` : `boolean` - deafult is True

```jac
config_details = jaseci.config_set(name,value,do_check);
```
### List Config

```jac
configs = jaseci.config_list();
```
### List Valid Config

```jac
valid_configs = jaseci.config_index();
```

### Configuration exits

`name` : `string` - name of configuration

```jac
config_exist = jaseci.config_exists(name);
```

### Delete Configurations

`name` : `string`
`do_check` : `boolean` - deafult is True
s
```jac
message = jaseci.config_delete(name,do_check);
```




