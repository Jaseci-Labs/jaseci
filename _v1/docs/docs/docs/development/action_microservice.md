---
sidebar_position: 4
---

# Running Action Library as a Service

In this tutorial, we will discuss how to use `uvicorn` to stand up a Jaseci action library as an independent server.
We use `jac_nlp` and `use_enc` for this example.

There are two ways to stand up a jaseci action server: via the python module or directly from the source code.

## Using the python package
After installing `jac_nlp` package.
* `pip install jac_nlp[use_enc]`

Run the following command to stand up the server.
* `uvicorn jac_nlp.use_enc:serv_actions`

Once run it should look like this once successful.
```
INFO:     Started server process [21349]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

To use it in your jaseci app, you will have to load the action using the following command.
* `actions load remote http://127.0.0.1:8000`

## Using the action source code
If you have access to the python file containing the source code for the action library, you can directly run it as a service.

In the case of `use_enc`, the source file is in the jaseci repo at `jaseci_ai_kit/jac_nlp/jac_nlp/use_enc/use_enc.py`

> **Note**
>
> You can use this process to stand up any custom jaseci action module

Navigate to the directory where the python file is and run

* `uvicorn [name_of_file]:serv_actions ` in this case `uvicorn use_enc:serv_actions`

You should see similar output as shown above.