# Test

In this tutorial, we will discuss how to use uvicorn to stand up a jaseci_ai_kit server locally.

Let's walk you through the process.

# Process
There are two ways to stand up a jaseci_ai_kit server and we will explore those in the following section.

## Through the installed jaseci_ai_kit pip package
After installing jaseci_ai_kit package.
* `pip install jaseci_ai_kit`
  
Run the following command to stand up the server.
* `uvicorn jaseci_ai_kit.[ai_model]:serv_actions`

We will stand up the cl_summer (summarization AI model). The command is as follow:
* `uvicorn jaseci_ai_kit.cl_summer:serv_actions`

Once run it should look like this once successful.
```
←[32mINFO←[0m:     Started server process [←[36m13024←[0m]
←[32mINFO←[0m:     Waiting for application startup.
←[32mINFO←[0m:     Application startup complete.
←[32mINFO←[0m:     Uvicorn running on ←[1mhttp://127.0.0.1:8000←[0m (Press CTRL+C to quit)
```

To use it in your jaseci app, you will have to load the action using the following command.
* `actions load remote http://127.0.0.1:8000`

Let's walk you through the other way.

## Through the repo
After you download the jaseci repo from git, the first step you will have to do is change the directory to one location below.

* `cd jaseci_kit/jaseci_kit/modules/cl_summer`

> **Note**
>
> You can use this process to stand up custom jaseci modules

To stand it up locally you will run the following command in terminal:

* `uvicorn [name_of_file]:serv_actions ` in this case `uvicorn cl_summer:serv_actions`

If you don't need the default port or host you can use this command:
* `uvicorn cl_summer:serv_actions --host 0.0.0.0 --port 9000`

After you run the command it should look like this, once it is successful.

```
←[33mWARNING←[0m:  ASGI app factory detected. Using it, but please consider setting the --factory flag explicitly.

←[32mINFO←[0m:     Started server process [←[36m42808←[0m]
←[32mINFO←[0m:     Waiting for application startup.
←[32mINFO←[0m:     Application startup complete.
←[32mINFO←[0m:     Uvicorn running on ←[1mhttp://0.0.0.0:9000←[0m (Press CTRL+C to quit)
```

After you see the server started you will have to go to the browser and run this domain:
* `http://0.0.0.0:9000/docs`

To use it in your jaseci app, you will have to load the action using the following command.
* `actions load remote http://0.0.0.0:9000` 

Congratulations, you have successfully use uvicorn to stand up a jaseci_ai_kit server locally.