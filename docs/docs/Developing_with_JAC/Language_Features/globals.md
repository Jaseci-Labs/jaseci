# Global Variables in Jaseci
Global variables are variables that can be accessed anywhere in your application. They can be useful for storing values that are used frequently or that need to be accessed from different parts of your code.

## Declaring a Global Variable
To declare a global variable in Jac, you can use the global keyword followed by the name of the variable and its initial value. For example:

```jac
//global variable_name = value
global transportation = "Airplane";
```
This tells the interpreter that the variable is a global variable and can be accessed from anywhere in your code.

## Accessing a Global Variable

To access a global variable in Jac, you use the syntax global.variable_name. For example:

```jac
//global.variable_name
walker init{
    transport_mode = global.transportation;
    std.out(transport_mode);
}
```
**Output**
```
Airplane
```
This syntax tells the interpreter to look for the variable in the global scope, rather than the local scope.

It's important to note that overusing global variables can make your code harder to understand and maintain, so use them judiciously. In general, it's a good practice to limit the scope of your variables to the smallest scope possible.

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