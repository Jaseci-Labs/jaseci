# **HOW TO TRIGGER TASK**

Any walker that can be called with `is_async` field

### **GET**
 - just add `is_async=true` on query param

### **POST** (just choose one)
 - add `is_async=true` query param
 - if json body, add `"is_async":true`
 - if multipart, add new field `is_async` value is equal to `true`

### **RESPONSE**
```json
{
    "task_id": "efd67095-a7a0-40db-8f89-6887ae56dbb3"
}
```

## **GET TASK STATE**
### **UNCONSUMED/RUNNING TASK**
`/js/walker_queue_check`

### **RESPONSE**
```json
{
    "scheduled": {
        "celery@BCSPH-LPA-0327": []
    },
    "active": {
        "celery@BCSPH-LPA-0327": []
    },
    "reserved": {
        "celery@BCSPH-LPA-0327": []
    }
}
```

### **SPECIFIC TASK**
`/js/walker_queue_check?task_id={{`**`task_id`**`}}`
 - status check only

`/js/walker_queue_wait?task_id={{`**`task_id`**`}}`
 - will forcely wait for the result

### **RESPONSE**
```json
{
    "state": "SUCCESS",

    // will show if result is available
    "result": {
        "success": true,
        "report": [
            ...
        ]
    }
}
```

# **HOW TO SETUP SCHEDULE**

## **SCHEDULED_WALKER**

 - Add periodic task
 - Select `jaseci.svc.task.common.ScheduledWalker`
 - set your schedule (interval, crontab, solar, clocked, start/end data are supported)
 - set argument with below kind of structure

### **ARGUMENT STRUCTURE**

```json
{
    // Required
    "name": "run",

    // Required
    "ctx": {},

    // Optional but may not have default
    // accepted value: urn | alias
    "nd": "active:graph",

    // Optional but may not have default
    // accepted value: urn | alias | global
    "snt": "active:sentinel",

    // Required
    // used also for getting aliases
    "mst": "d6851f2a-e4a1-4fca-b582-9db5e146af59"
}
```

----
# **OPTIONAL FEATURES**

## **SCHEDULED_SEQUENCE**

 - Add periodic task
 - Select `jaseci.svc.task.common.ScheduledSequence`
 - set your schedule (interval, crontab, solar, clocked, start/end data are supported)
 - set argument with below kind of structure

### **ARGUMENT STRUCTURE**

```json
{
        // optional if you just want to add default values
        "persistence": {
            "additional_field": "can_be_call_via_#.additional_field",
        },

        // not recommended to use but possible
        "container": {
            // act as previous response
            "current": {},

            // will auto generate for the loop :: all of these are optional
            "parent_current": {},
            "index": {},
        },

        "requests": [{
            "method": "POST",
            "api": "http://localhost:8000/user/token/",
            "body": {
                "email": "dummy@dummy.com",
                "password": "Bcstech123!"
            },

            // save to persistence
            // accessible via #.login / #.login_req
            "save_to": "login",
            "save_req_to": "login_req"
        },

        {
            "method": "POST",
            "api": "http://localhost:8000/js_admin/master_allusers",
            "body": {
                "limit": 0,
                "offset": 0
            },
            "header": {

                // $ == previous response
                "Authorization": "token {{$.token}}"

            },

            // by default exception will break the loop
            // ignore_error true will continue the loop/sequence even exception occured
            "ignore_error": true,

            // initialize loop after the current block trigger
            "__def_loop__": {

                // $ == current response
                // $.path.to.your.array !! required to be an array
                "by": "$.data",

                // filter structure
                // supports `or` and `and` operator.
                // filter = [] is default to `and` operator
                "filter": [{
                    "or": [{
                        "by": "$.user",
                        "condition": {

                            // optional constraints
                            // can be remove if not needed
                            "eq": "dummy+testing3@dummy.com",
                            "ne": null, "gt": null, "gte": null,
                            "lt": null, "lte": null, "regex": null

                        }
                    }, {
                        "and": [{
                            "by": "$.user",
                            "condition": {
                                "eq": "dummy+testing2@dummy.com"
                            }
                        }, {
                            "by": "$.jid",
                            "condition": {
                                "eq": "urn:uuid:29cba0c9-e24e-4d15-a2b6-4354c59a4c86"
                            }
                        }]
                    }]
                }],

                // nested request used for the loop
                // same mechanism from requests above
                "requests": [{
                        "method": "POST",
                        "api": "http://localhost:8000/js/object_get",
                        "body": {
                            // $ on first request on loop is from current response from the looper
                            "obj": "{{$.jid}}",
                            "depth": 0,
                            "detailed": true
                        },
                        "header": {
                            // # == persistence
                            "Authorization": "token {{#.login.token}}"
                        },
                        "ignore_error": true,

                        // ! == current index :: default 0
                        "save_to": "object_get_{{!}}",

                        // nested loop is supported
                        "__def_loop": ...
                    },
                    {
                        "method": "POST",
                        "api": "http://localhost:8000/js/walker_run",
                        "body": {
                            "name": "get_botset",
                            "ctx": {},
                            "nd": "{{$.active_gph_id}}",
                            "snt": "active:sentinel"
                        },
                        "header": {
                            "Authorization": "token {{#.login.token}}"
                        },

                        // @ == the current index `data` on the loop
                        "save_to": "response_{{@.jid}}",
                        "save_req_to": "req_{{@.jid}}"
                    }
                ]
            }
        },
        {
            "method": "GET",
            "api": "https://jsonplaceholder.typicode.com/todos/100",
            "save_to": "testing_nested",
            "save_req_to": "req_testing_nested"
        },
        {
            // Trigger will use jaseci interface
            "method": "JAC",
            "api": "master_allusers",
            "body": {
                "limit": 0,
                "offset": 0
            },
            // Optional: if master is present trigger is
            // considered authenticated or general else public
            "master": "{{#.master}}", // will use persistence.master
            "save_to": "master_allusers_by_walker"
        }
    ]
}
```