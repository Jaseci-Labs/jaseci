# Stand up a jaseci_ai_kit server locally

In this tutorial, we will discuss how to use uvicorn to stand up a jaseci_ai_kit server locally and quickly

Are you Excited? Let's jump right in.

# Process
First, you will have to cd into the path of the jaseci_ai_kit module for example let try to stand up cl_summer AI module. From the root jaseci directory run this command in the terminal as follows:

* `cd jaseci_kit/jaseci_kit/modules/cl_summer`

You can CD into any AI models, after you go into the cl_summer directory you will have to stand it up locally and how you do that you will run the following:

* `uvicorn [name_of_file]:serv_actions ` in this case `uvicorn cl_summer:serv_actions`

If you don't want the default port and host you can use this command:
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

Congratulations, you have successfully use uvicorn to stand up a jaseci_ai_kit server locally.