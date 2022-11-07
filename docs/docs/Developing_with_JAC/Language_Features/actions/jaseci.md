# Jaseci Actions
## Alias
Alias provides names  for long string like UUIDs.

### Register Alias 
```jac 
#name (str): The name for the alias created by caller.
#value (str): The value for that name to map to (i.e., UUID)
response  = jaseci.alias_register(name,value);

```
### List Aliases
```jac 
# List all string to string alias that caller can use
jaseci.alias_list()

```

### Delete Alias 

```jac
# Delete an active string to string alias mapping
# name (str): The name for the alias to be removed from caller.
jaseci.alias_delete()
```
### Clear Alias
```jac 
#  Removes  all aliases.
jaseci.alias_clear()

```
## Objects

### Get global Variable
```jac 
# name: name of global variable
value = jaseci.global_get(name);

```

### Object Details 
```jac
# retuen detail of jaseci object
object : element - jaseci object
details = jaseci.object_get(object);
```

### Object Access Mode 

```jac 
# Get the object access mode for any jaseci object.
# object : element - jaseci object
accessMode  = jaseci.object_perms_set(object)

```

### Set Object access mode 

```jac 
# valid perms = ["public", "private", "read_only"]
# object : element - jaseci object
# perm : string 
jaseci.object_perms_set(element,perm);
```

### Object access grant

```jac
# grants one object the acess to another object
# object : element - object to access
# master : element  - object to gain access

rent = jaseci.object_perms_grant(element, master);

```
### Revoke object access

```jac
#Remove permissions for user to access a Jaseci object
# object : element - object that was  accessed
# master : element  - object that has access.
ret = jaseci.object_perms_revoke(element,master);

```
## Graphs

### Create Graph
```jac
# Create a graph instance and return root node graph object
jaseci.graph_create()

```
### Get Graph Content
```jac 
# Return the content of the graph with mode
# Valid modes: {default, dot, }
# gph :graph - graph whose conten you need
# mode : string - "deafult" or "dot" , "default" by default
Contents = jaseci.graph_get(gph);

```
### List Graph Objects

```jac
#  Provide complete list of all graph objects (list of root node objects)
# detailed : boolean - if eac graph details are wanted
graph_info = jaseci.graph_list(detailed);

```
### Set Default Graph
```jac 
# set the default graph master should use
# gph : graph - graph to be default.
message = jaseci.graph_active_set(gph);

```
### Remove Default Graph
```jac 
# Unsets the default sentinel master should use
jaseci.graph_active_unset();
```

### Get Default Graph 
```jac
# detailed : boolean - default false , true to return graph details (optional)
grph = jaseci.graph_active_get()
```
### Delete Graph 
```jac 
# permantely  delete graph 
# grph : graph - graph to be deleted

message = jaseci.graph_delete(grph);
```
### Return Node Value
```jac 
# returns value of a given node
# nd : node : node whose value will be returned.
node_value =  jaseci.graph_node_get(nd);
```
### Set Node Value
```jac 
# Assigns values to member variables of a given node using ctx object
# nd : node : node to who a value will be assigned.
# ctx : dictionary - values to assign 

node_details = jaseci.graph_node_set(nd,ctx);
```
## Sentinels

### Register Sentinel 
```jac 
#Create blank or code loaded sentinel and return object
# name: str -  "default" when not specified,
#encoded: bool 
#auto_run: Auto_run is the walker to execute on register (assumes active graph is selected), default is "init"
#ctx: dict = {},
#set_active: bool = True,

sentel = jaseci.sentinel_regsiter(name,encoded,auto_run,ctx,set_active);

``` 

### Global Sentinel 
```jac 
#   Copies global sentinel to local master
#set_active : boolean - set sentinel to be active
# on_demand : boolean - 

sentl = jaseci.sentinel_pull(set_active);
```


### Get Sentinel 
```jac 
# Get a sentinel rendered with specific mode
#Valid modes: {default, code, ir, }
#snt : sentinel : sentinel to be rendered in specific mode.
#mode : str - mode sentinel will be in 
snt  = jaseci.sentinel_get(snt,mode);
```
### Set Sentinel Code
```jac 
# Set code/ir for a sentinel, only replaces walkers/archs in sentinel
# Needs more clarity
jaseci.sentinel_set();
```
### Sentinel List
```jac 
# Provides Completed list of all sentinel objects 

#snt_list = jaseci.sentinel_list();
```
### Sentinel Test
```jac 
# Run battery of test cases within sentinel and provide result
#snt : sentinel - sentinel to be tested

snt_details = jaseci.sentinel_test(snt);
```
### Default Sentinel
```jac
# Sets the default sentinel master should use
#snt :sentinel - sentinel to be made default

message = jaseci.sentinel_active_set(snt);
```

### Remove Default Sentinel
```jac 
# Unsets the default sentinel master should use
messsage = jaseci.sentinel_active_unset();
```

### Set Global Sentinel 
```jac 
# Sets the default master sentinel to the global sentinel
response  = jaseci.sentinel_active_global();
```
### Return default Sentinel
```jac 
#  Returns the default sentinel master is using
response = jaseci.sentinel_active_get();
```

### Delete Sentinel
```jac 
# Permanently delete sentinel with given id
snt : sentinel - sentinel to be deleted

message = jaseci.sentinel_delete(snt);
```
### Run Walker
```jac 
# clarity needed
# Run a walker on a specific node
# wlk : walker - walker to be ran 
# nd : node -  node where walker will be placed
# ctx : dictionary  - context for walker
response  = jaseci.walker_summon()
```

### Register Walker 
```jac 
# clarity needed
#  Create blank or code loaded walker and return object
walker_seralized = jaseci.walker_register();
```
### Get Walker 
```jac 
# Get a walker rendered with specific mode
# wlk : walker - walker to be rendered 
# mode : str - mode to return walker
#  Valid modes: {default, code, ir, keys, }
wlk_response = jaseci.walker_get(wlk,mode);
``` 
### Set Walker code
```jac 
#  Set code/ir for a walker
# Valid modes: {code, ir, }
# wlk :walker - walker code/ir to be set
# code : str - "code" or  "ir" 
message = jaseci..walker_set(wlk,code);
```

### List Walkers
```jac 
# List walkers known to sentinel
snt :sentinel - active sentinel

walkers = jaseci.walker_list();

```
### Delete Walker 
```jac 
# Permantely delete walker with given id 
# wlk : walker - walker to be deleted
# snt : sentinel - sentinel where walker resides
message = jaseci.walker_delete(wlk,snt);
```

### Spawn Walker 
```jac 
#  Creates new instance of walker and returns new walker object
# name : str - name of walker
# snt : sentinel - sentinel the walker will be under
spawn_wlk = jaseci.walker_spawn_create(name,snt);
```

### Delete spawned Walker
```jac 
#Delete instance of walker 
# name : string - name of walker to be deleted
jaseci.walker_spawn_delete(name);
```

### List Spawned walker 
```jac 
# List walkers spawned by master
# detailed : boolean - return details of walkers
walkers  = jaseci.walker_spawn_list(deatailed);
```

### Assign walker to node 
```jac 
#  Assigns walker to a graph node and primes walker for execution 
# wlk : walker  - walker to be assigned
# nd : node - node walker will be assigned too
# ctx : dicionary  - context for node

message   = jaseci.walker_prime(wlk,nd,ctx);
```


### Execute Walker 
```jac 
# execute walker assuming it is primed.
# wlk : walker -  walker to execute
# nd : node - node where execution will begin

response  = jaseci.walker_execute(wlk,nd);
```

### Walker run
```jac 
# Creates walker instance, primes walker on node, executes walker, reports results, and cleans up walker instance.
#name: str - name of the walker 
#nd: node = Node walker will be primed on 
#ctx: dict -  {} by default
#snt: sentinel - None  by default 
#profiling: bool - False by default

response =  jaseci.walker_run(name,nd,ctx,snt,profiling);
```

### Walker Individual APIs
```jac 
#name : string - name of walker
#nd :node - node walker will be primed on
# ctx : dictionary - dictionary for context information
# snt :  sentinel , none by default
# profiling : boolean , false by default
 response = jaseci.wapi(name,nd,ctx);
 ```

## Architypes

### Create Architype

```jac 
# code : string : the test or filename  for an architype jac code
#encoded : boolean : if code is encoded or not
# snt (uuid) : the uuid of the sentinel to be the owner of this architype

architype_response  = jaseci.architype_register(code,encoded,snt);

```

### Get Architype 

```jac 
# Get an architype rendered with specific mode
# arch : architype - the architype being accessed
# mode : string - valid modes {default, code, ir}
# detailed : boolean - return detailed info also

architpe_serialized   = jaseci.architype_get(arch,mode,detailed);
```
### Set Architype code or ir
```jac 
#arch (uuid): The architype being set
#code (str): The text (or filename) for an architypes Jac code/ir
#mode (str): Valid modes: {default, code, ir, }

response  = jaseci.architype_set(arch,code,mode);
```
### List Architype 
```jac 
# List architypes know to sentinel
#snt (uuid): The sentinel for which to list its architypes
# detailed (bool): Flag to give summary or complete set of fields

archs = jaseci.architype_list(snt,detailled);
```

### Delete Architype
```jac 
# Permanently delete sentinel with given id
#arch (uuid): The architype being set
#snt (uuid): The sentinel for which to list its architypes

response = jaseci.architype_delete(arch,snt);
```


## Masters

### Create Master 
```jac 
# create a master instance and retrun root node master object 
# name  :str - name of master
# active : boolean 
# ctx : dictionary - additional feilds for overloaded interfaces

master_object  = jaseci.master_create(name,active,ctx);
```

### Get Master Content 
```jac 
# return the content of the master with mode
# name : string - name of master to be returned
# mode : string - modes{'default',}

master_object = jaseci.master_get(name,mode);
```

### List Masters
```jac 
#  Provide complete list of all master objects (list of root node objects)
# detailed : boolean - detailed info wanted. 

masters  = jaseci.master_list(detailed);
```

#### Set Default Master
```jac 
#  Sets the default sentinel  master should use
# name  : name of master to be set

response  = jaseci.master_active_set(name);
```

### Unset Default Master 
```jac 
# unsets the default sentinel mastershould use
response  = jaseci.master_active_unset();
```

### Get Default Master
```jac 
#  Returns the default master master is using
# detailed : boolean  - return detailed information on the master

master_serialized = jaseci.master_active_get(detailed);
```
### Get Master Object
```jac 
# Returns the masters object

master_object = jaseci.master_self();
```
### Delete Master
```jac 
name : str - master to be deleted

response   = jaseci.master_delete(name);
```

## Logger 
APIs for Jaseci Logging configuration
### Connect to internal logger
```jac 
#   Connects internal logging to http(s) (log msgs sent via POSTs)
#  Valid log params: {sys, app, all }
# host : string  - 
# port : string - 
# url : string - 
# log : string  - 
response = jaseci.logger_http_connect(host,port,url,log);
```
### Remove HTTP Handler
```jac 
# log  : string - default ,all

response  = jaseci.logger_http_clear(log);

```
### Check Active logger
```jac 
#  list active loggers

response = jaseci.logger_list();
```

## Global API

### Set Global 
```jac 
# Set a global variable 
# name  : string - name of global
# value : string -  value of global
 response = jaseci.global_set(name,value);
```
### Delete Global 
```jac 
# delete a global
# name : string - delete globals
response = jaseci.global_delete(name);
```
### Set Global Sentinel 
```jac 
# set sentinel as  globally accessible
# snt : sentinel -  sentinel to be set globally accessible
response = jaseci.global_sentinel_set(snt);
```
### Unset Global Sentinel
```jac 
#unset globally accessible variable
# snt : sentinel - sentinel to be removed as globally acccessible 
response  = jaseci.sentinel_unset(snt);
```
 
## Super Master

### Super Instance of Master
```jac 
#   Create a super instance and return root node super object
# name : string - name of master
# set_active : boolean - set master to active
# other_fields : dictionary - used for additional feilds for overloaded interfaces (i.e., Dango interface)

master_object  = jaseci.master_createsuper(name,set_active,other_fields);
```
### Masters info
```jac 
#  Returns info on a set of users
# num : int -  specifies the number of users to return 
# start_idx :int -  specfies where to start

# in development 
```

### Set Default Master
```jac 
# Sets the default master master should use
# mast : master - master to be used
response  = jaseci.master_become(mast);
```

### Unset  default Master

```jac 
# Unsets the default master master should useS
response = jaseci.master_become();
```

## Stripe   
 Set of APIs to expose Stripe Management

 ### Create Product 
 ```jac 
 # name : string - default "VIP Plan"
 # description : string - default " Plan description"

 message = jaseci.stripe_product_create(name,desciption);
 ```

### Modify Product Price 
```jac 
# productId : string - id of product to be modified 
# amount : float - amount for product ,default is 50
# interval : string - default  "month"

message = jaseci.stripe_product_price_set(productId,amount,interval);
```

### List Products 
```jac 
# retrieve all products
# detailed : boolean - details of all products
 product_list = jaseci.stripe_product_list();
 ```

 ### Create Customer 
 ```jac 
 # paymentId : string - id of payment method
 # name : string - name of customer 
 # email : string - email of customer
 # description : string  - description of customer

 message =  jaseci.stripe_customer_create(paymentId,name,email,description);
 ```
### Get Customer Information
```jac 
# retrieve customer information
#customerId : string - id to identify customer

message = jaseci.stripe_customer_get(customerId);
```

### Add Customer Payment Method
```jac 
# paymentMethodId : string - id of payment method
# customerId  : string - id to uniquely identify customer 
message = jaseci.stripe_customer_payment_add(paymentId,customerId);
```

### Remove Customer Payment method
```jac 

# paymentMethodId : string - id of payment method

message = jaseci.stripe_customer_payment_delete(paymentId);
```

### Customer's List of payment Method
```jac 
# get list of customer payment method
# customerId : string - id to uniquely identify customer

payment_methods = jaseci.stripe_customer_payment_get(customerId);
```
### Update Customer default payment
```jac 
# paymentMethodId : string - id of payment method
# customerId  : string - id to uniquely identify customer 

message = jaseci.stripe_customer_payment_default(customeId,paymentMethodId);
```

### Create Customer Subscription
```jac 
# create customer subscription
# paymentId : string - id pf payment method
# priceId : string - id for price 
# customerId: string - id to uniquely identify customer 

message = jaseci.stripe_subscription_create(paymentId,priceId,customerId);
```

### Cancel Customer Subscription
```jac 
# subscriptionId : string - id to uniquley identify subscription
message  = jaseci.stripe_subscription_delete(subscriptionId);
```
### Get Customer Subscription 
```jac 
# retrieve customer subscription 
# customerId : string - id to uniquely identify customer

customer_subscription = jaseci.stripe_subscription_get(customerId);
```

### Invoice List
```jac 
# retrieve customer list of invoices
# customerId : string - id to uniquely identify customer`
# subscriptionId : string - id to uniquley identify subscription
# limit : int - max amount of invoices to return
# lastitem : string - id of item from where the return should start default is " " 

invoices = jaseci.stripe_invoice_list(customerId,subscriptionId,limit,lastitem);
```
### Load actions 

## Load modules locally
```jac 
# hot load a python module and assimlate any jaseci action
# file  string - module to be loaded
success_message  = jaseci.actions_load_local(file);
```
### Load modules remote
```jac 
#  Hot load an actions set from live pod at URL
# url : string - link to module to be loaded
success_message = jaseci.actions_load_remote(url);
```
### Load modules local
```jac
mod : string - name of module to be loaded

success_messsage = jaseci,actions_load_module(mod);
```
### List actions
```jac 
actions = jaseci.actions_list();
```
## Configurations APIs

### Get config
```jac 
# get a Connfig
# name : string - name of configurations
# do_check : boolean - deafult is True

confid_details = jaseci.config_get(name,do_check);
```
###  Set Config
```jac 
# name :string - name of configuration
# value : string - value to set 
# do_check : boolean - deafult is True

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
```jac 
# name : string - name of configuration
config_exist = jaseci.config_exists(name);
```
### Delete Configurations 
```jac 
#name : string
# do_check : boolean - deafult is True

message = jaseci.config_delete(name,do_check);
```




