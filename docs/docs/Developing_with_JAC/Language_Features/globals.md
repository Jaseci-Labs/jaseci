# **Global Reference Syntax** (to be improve)

This for accessing current thread attributes.

## **`global.context` \<Dict\>**

It will return global variables

## **`global.info` \<Dict\>**
 - report
 - report_status
 - report_custom
 - request_context
 - runtime_errors

> **global.info[`"report"`]**
>
> returns current report list
> ```json
>    [1, "any value from report", {}, true, []]
> ```
> ---
> **global.info[`"report_status"`]**
>
> returns http status code for the report
> ```json
>    200
> ```
> ---
> **global.info[`"report_custom"`]**
>
> returns current report:custom value
> ```json
>    {
>        "yourCustomField": "customValue"
>    }
> ```
>
> ---
> **global.info[`"request_context"`]**
>
> returns current request payload
> ```json
>    {
>        "method": "POST",
>        "headers": {
>            "Content-Length": "109",
>            "Content-Type": "application/json",
>            "Host": "localhost:8000",
>            "User-Agent": "insomnia/2022.4.2",
>            "Accept": "*/*"
>        },
>        "query": {},
>        "body": {
>            "name": "sample_walker",
>            "ctx": {
>                "fieldOne": "1"
>            },
>            "nd": "active:graph",
>            "snt": "active:sentinel"
>        }
>    }
> ```
> ### **Usage:**
> walker can now accept custom payload (non ctx structure). Request body can be access via `globa.info["request_context"]["body"]`
> developers now have control on different request constraints such us method type and headers validation
>
> ---
> **global.info[`"runtime_errors"`]**
>
> returns current runtime error list
> ```json
>[
>   "sentinel1:sample_walker - line 100, col 0 - rule walker - Internal Exception: 'NoneType' object has no attribute 'activity_action_ids'"
>]
> ```
> ---