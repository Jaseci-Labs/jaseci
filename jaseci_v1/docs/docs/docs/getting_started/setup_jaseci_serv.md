---
sidebar_position: 2
description: A guide to setup Jaseci Server.
---

# Setting up Jaseci Server

Jaseci Server allows for the development of APIs to interact with your JAC Program.

## Step 1: Installing

To Install Jaseci Server run following in a bash terminal;

```bash
pip install jaseci-serv
```

## Step 2: Setting up database

After installing the Jaseci Server, you have to setup the database;

```bash
jsserv makemigrations base
jsserv makemigrations
jsserv migrate
```

This will create a database that will be used to run a jaseci instance of our application. Install the Schema and Database. It creates a `mydatabase` file in your working directory.

## Step 3: Starting the server

Start the server;

```bash
jsserv runserver 0.0.0.0:8000
```
If everything is fine you will see following in the terminal;

```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
April 26, 2023 - 01:36:28
Django version 3.2.18, using settings 'jaseci_serv.settings'
Starting development server at http://0.0.0.0:8000/
Quit the server with CONTROL-C.
```

Visit localhost:8000 from your favourite browser to access the server.

## Step 4: Creating Super User Account

Let's now spawn 2 new terminal in our current working directory.
In new terminal 1

Create an account for the server.

```bash
jsserv createsuperuser
```

You will be prompted to enter an email and password.

In new  terminal 2

## Step 5: Logging to Super User Account

Start jsctl, Run;

```bash
jsctl
```

Login to Jaseci Shell

```bash
jaseci> login http://localhost:8000
```

login with the credentials used to create the super user earlier. After successfully logging in, you will see a token that you will require later.

```
Token: 65eb08dfa3e31c770a203a87e37f047db81b3cf0123458b9062d2ed099193d7d
Login successful!
```
To get the token via postman; open up Postman

* Grab a token from Jaseci that represents an active session of the super user. Make a Post request to user/token
* Body of the request is as follows:

```
{
"email" : "email@gmail.com",
"password" : "password"
}
```
If everything goes well the post request will return with the following response;

```json
{
  "expiry": null,
  "token": "0877c50e1f2cb284609b8ee2b5cd6c35c615e8d3791cacca820a1ed0af3d3806"
}
```

Copy token returned from the response and save it somewhere.

* Grab a token from Jaseci that represents an active session of the super user. Make a Post request to user/token
* Body of the request is as follows:

```
{
"email" : "email@gmail.com",
"password" : "password"
}
```
If everything goes well the post request will return with the following response;

```json
{
  "expiry": null,
  "token": "0877c50e1f2cb284609b8ee2b5cd6c35c615e8d3791cacca820a1ed0af3d3806"
}
```

Copy token returned from the response and save it somewhere.

## Step 6: Running a Jac Program in the Server

Let's use a simple hello world program to demonstrate Jaseci Server;

```jac
walker init{
    std.out("Hello World");
}
```

Save the above program as `main.jac` and compile it program to JIR bit

```bash
jaseci> jac build main.jac
```

### Step 6.1: Register a new Sentinel

To register a new sentinel for compiled `main.jir`

```bash
jaseci> sentinel register -name main -mode ir main.jir
```

You'll see following output;

```json
Hello World
[
  {
    "version": null,
    "name": "main",
    "kind": "generic",
    "jid": "urn:uuid:21009aca-496b-42ff-ab41-83698158cba4",
    "j_timestamp": "2023-04-26T03:48:10.780607",
    "j_type": "sentinel",
    "code_sig": "eb068084a74ba42057ef98174d7906ed"
  },
  {
    "name": "root",
    "kind": "node",
    "jid": "urn:uuid:b9831f6c-e2b4-45cd-94b4-853a7779e8e5",
    "j_timestamp": "2023-04-26T03:48:10.780764",
    "j_type": "graph",
    "context": {}
  }
]
```

To show the entities in the code run;

```bash
jaseci> alias list
```
You will see output similar to this;

```json
{
  "active:graph": "urn:uuid:b9831f6c-e2b4-45cd-94b4-853a7779e8e5",
  "sentinel:main": "urn:uuid:21009aca-496b-42ff-ab41-83698158cba4",
  "main:architype:root": "urn:uuid:d0dd0fe9-9bc4-4073-baa8-762d96b90046",
  "main:architype:generic": "urn:uuid:454f180b-b162-4c3a-ac65-408d28939bc2",
  "main:walker:init": "urn:uuid:d6d3fc7b-1fff-433c-994f-e28b1073fc49",
  "active:sentinel": "urn:uuid:21009aca-496b-42ff-ab41-83698158cba4"
}
```

Copy the sentinel active sentinel ID , we will need it later.

