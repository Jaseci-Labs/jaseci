# Build a Custom Jaseci Module

In this tutorial, you are going to learn how to build a custom jaseci module with python. In this application I will teach you how to create a basic calculator module for jaseci.

Excited? Hell yeah! Let's jump in.

## Preparation
Let's start by creating a folder called `calculator` in your root directory of your application. After creating the folder let's create a file name `calculator.py` inside of the `calculator` folder.

> **Note**
>
> we are using python to create the custom jaseci module so you will need .py files and not jac.

After creating the file, open the file in a code editor and let's start coding our module.

```py
from jaseci.actions.live_actions import jaseci_action
```
First, we will have to import jaseci_actions to the `calculator.py` file. We will be using jaseci actions to load the module into jaseci.

```py
@jaseci_action(act_group=["timestamp"], allow_remote=True)
```
In this block:
- `act_group` is the name of the jaseci action group called when loading a the module.
- `allow_remote` indicates whether you want this action to be run remotely or not.


We will be adding onto the file.
```py
@jaseci_action(act_group=["timestamp"], allow_remote=True)
def add(first_number: int, second_number: int):
    return first_number + second_number
```

What this functions does, it adds the two numbers from the parameter and returns the sum of each number.

> **Note**
>
> Practice adding data type to the parameters for e.g. `first_number: int` because jaseci_actions use this as validation, remotely and also through the jaseci application.  

## Loading the custom module (API)
In this section, I will run you through how to load the custom module through the API.
```bash
> uvicorn calculator:serv_actions 
```

We use uvicorn to run modules remotely.

> **Note**
>
> `calculator` is folder name and the path in which the module is located and `serv_actions` will allow you to run all functions remotely at one time.


```
←[33mWARNING←[0m:  ASGI app factory detected. Using it, but please consider setting the --factory flag explicitly.
←[32mINFO←[0m:     Started server process [←[36m15604←[0m]
←[32mINFO←[0m:     Waiting for application startup.
←[32mINFO←[0m:     Application startup complete.
←[32mINFO←[0m:     Uvicorn running on ←[1mhttp://127.0.0.1:8000←[0m (Press CTRL+C to quit)
```

You will see something like this and if it shows this you are ready to test out the jaseci custom module.

Go to http://localhost:8000/docs and you can test out your module to see if it works remotely.

# Loading the custom module (JAC)
In this section, I will run you through how to load the custom module through the Jac application.

```bash
> actions load local calculator/calculator.py
```

Since we are creating our own module we have to use the term `local` instead of module or remote. After local is the path to where the module is located.

```
{
  "success": true
}
```
You should see this after running the command. If you see this you have successfully build a custom module using jac with Jaseci.

# How to use the custom module (JAC)
In this section we will show you how to use the custom module in the jac application.

Create a file name main.jac and add the following code.

```js
walker init {
    can calculator.add;
    report calculator.add(1,1);
}
```

This allows you to load the module `can (act_group created)(function created for the act_group);`
``` js
can calculator.add;
```

We will report the result from the calculation.
``` js
report calculator.add(1,1);
```

The following will be the result after running the init walker.
```bash
{
  "success": true,
  "report": [
    2
  ],
  "final_node": "urn:uuid:04e97f70-26b3-467e-a291-bd03b18e7a6d",
  "yielded": false
}
```

Once you see that status it means that everything is working perfectly. Simple right! Hope you learn't something new today.
