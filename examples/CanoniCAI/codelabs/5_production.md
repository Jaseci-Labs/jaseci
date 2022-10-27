# Bring Your Application to Production
Typing in questions and getting responses via `jsctl` in terminal is a quick and easy way of interactively test and use your program.
But the ultimate goal of building any products is to eventually deploying it to production and having it serve real users via standard interface such as RESTful API endpoints.
In this section, we will cover a number of items related to bringing your jac program to production.

## Introducing `yield`
`yield` is a jac keyword that suspend the walker and return a response, which then can be resumed at a later time with the walker context retained.
Walker context includes its `has` variables and its node traversal plan (i.e., any nodes that have been queued by previously executed `take` statements).
This context retention is done on a per-user basis.
`yield` is a great way to maintaining user-specific context and history in between walker calls.
To learn more about `yield,` refer to the relevant sections of the Jaseci Bible.

In the case of our conversational AI system, it is essential for our walker to remember the context information gained from previous interactions with the same user.
So let's update our walker with `yield.`

```jac
walker talk {
    has question, interactive = false;
    has wlk_ctx = {
        "intent": null,
        "entities": {},
        "prev_state": null,
        "next_state": null,
        "respond": false
    };
    has response;
    root {
        take --> node::dialogue_root;
    }
    cai_state {
        if (!question and interactive) {
            question = std.input("Question (Ctrl-C to exit)> ");
            here::init_wlk_ctx;
        } elif (!question and !interactive){
            std.err("ERROR: question is required for non-interactive mode");
            disengage;
        }
        here::nlu;
        here::process;
        if (visitor.wlk_ctx["respond"]) {
            here::nlg;
            if (interactive): std.out(response);
            else {
                yield report response;
                here::init_wlk_ctx;
            }
            question = null;
            take here;
        } else {
            take visitor.wlk_ctx["next_state"] else: take here;
        }
    }
}
```
Two new syntax here:
* `report` returns variable from walker to its caller. When calling a walker via its REST API, the content of the API response payload will be what is reported.
* `yield report` is a shorthand for yielding and reporting at the same time. This is equivalane to `yield; report response;`.

## Introduce `sentinel`
`sentinel` is the overseer of walkers, nodes and edges.
It is the abstraction Jaseci uses to encapsulate compiled walkers and architype nodes and edges.
The key operation with respesct to `sentinel` is "register" a sentinel.
You can think of registering a `sentinel` as a compiling your jac program.
The walkers of a given sentinel can then be invoked and run on arbitrary nodes of any graph.

Let's register our jac program
```bash
jaseci > sentinel register tesla_ai.jir -set_active true -mode ir
```

Three things are happening here:
* First, we registered the `jir` we compiled earlier to new sentinel. This means this new sentinel now has access to all of our walkers, nodes and edges. `-mode ir` option speciifes a `jir` program is registered instead of a `jac` program.
* Second, with `-set_active true` we set this new sentinel to be the active sentinel. In other words, this sentinel is the default one to be used when requests hit the Jac APIs, if no specific sentinels are specified.
* Third, `sentinel register` has automatically creates a new `graph` (if no currently active graph) and run the `init` walker on that graph. This behavior can be customized with the options `-auto_run` and `-auto_create_graph`.

To check your graph
```bash
jaseci > graph get -mode dot
```
This will return the current active graph in DOT format.
This is the same output we get from running `jac dot` earlier.
Use this to check if your graph is successfully created.

Once a sentinel is registered, you can update its jac program with
```bash
jaseci > sentinel set -snt SENTINEL_ID -mode ir tesla_ai.jir
```

To get the sentinel ID, you can run one of the two following commands
```bash
jaseci > sentinel get
```
or
```bash
jaseci > sentinel list
```
`sentinel get` returns the information about the current active sentinel, while `sentinel list` returns all available sentinels for the user.
The output will look something like this
```json
{
  "version": null,
  "name": "main.jir",
  "kind": "generic",
  "jid": "urn:uuid:817b4ff4-e6b7-4296-b383-55515e1e8b4a",
  "j_timestamp": "2022-08-04T20:23:16.952641",
  "j_type": "sentinel"
}
```
The `jid` field is the ID for the sentinel. (`jid` stands for jaseci ID).

With a sentinel and graph, we can now run walker with
```bash
jaseci > walker run talk -ctx "{\"question\": \"I want to schedule a test drive\"}"
```
And with `yield`, the next walker run will pick up where it leaves off and retain its variable states and nodes traversal plan.

## Tests
Just like any program, a set of automatic tests cases with robust coverage is essential to the success of the program through development to production.
Jac has built-in tests support and here is how you create a test case in jac.

```jac
import {*} with "tesla_ai.jac";

test "testing the Tesla conv AI system"
with graph::tesla_ai by walker::talk(question="Hey I would like to go on a test drive"){
    res = std.get_report();
    assert(res[-1] == "To set you up with a test drive, we will need your name and address.");
}
```
Let's break this down.
* `test "testing the tesla conv AI system"` names the test.
* `with graph::tesla_ai` specify the graph to be used as the text fixture.
* `by walker::talk` specify the walker to test. It will be spawned on the anchor node of the graph.
* `std.get_report()` let you access the report content of the walker so that you can set up any assertion neccessary with `assert`.

To run jac tests, save the test case(s) in a file (say `tests.jac`) and import the neccessary walkers and graphs. Then run
```bash
jaseci > jac test tests.jac
```
This will execute all the test cases in `tests.jac` squentially and report success or any assertion failures.

## Running Jaseci as a Service
So far, we have been interacting jaseci through `jsctl`.
jaseci can also be run as a service serving a set of RESTful API endpoints.
This is useful in production settings.
To run jaseci as a service, first we need to install the `jaseci-serv` python package.

```bash
pip install jaseci-serv
```
> **Important**
>
> As a best practice, it is recommended to always use the same jsctl version (installed as part of the jaseci package) and jsserv version (installed with the jaseci-serv python package). You can install a specific version of either package via `pip install PACKAGE_NAME==PACKAGE_VERSION`.

Since this is the first time we are running a jaseci server, a few commands are required to set up the database
```bash
jsserv makemigrations base
jsserv makemigrations
jsserv migrate
```
The above commands essentially initializes the database schemas.

> **Important**
>
> The above commands are only required the first time you are starting a jsserv instance. These commands will create a `mydatabase` file in the current directory as the storage for the database.

We will also need an admin user so we can log into the jaseci server. To create an admin user, run
```bash
jsserv createsuperuser
```
And follow the command line prompts to create a super user.

Then launch the jaseci server with
```bash
jsserv runserver
```

You should see an output that looks like the following

```bash
$ jsserv runserver
Watching for file changes with StatReloader
Performing system checks...
System check identified no issues (0 silenced).
October 24, 2022 - 18:27:14
Django version 3.2.15, using settings 'jaseci_serv.jaseci_serv.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

Take note of the `http://127.0.0.1:8000/`. This is the URL of your jsserv instance.
In this case, `127.0.0.1` means it is live on localhost.

To access the server via `jsctl`, we just need to login to the server first before running any jsctl commands
```bash
jsctl
jaseci > login http://localhost:8000/
Username:
Password:
```
Follow the prompts the provide the email and password you used to create the superuser earlier.
If logged in successfully, you should see a token being returned.
It will look something like this
```bash
jaseci > login http://localhost:8000
Username: yiping@jaseci.org
Password:
Token: 45ef2ac9d07aa571769c7d5452e4553a8a74b061ea621e21222789aa9904e8c7
Login successful!
@jaseci >
```
> **Important**
>
> Notice the `@` symbol in front of the `@jaseci >` command line prompt. This indicates that your jsctl session is now logged into a jsserv instance, while `jaseci >` indicates it is in a local session.

While logged into the jsserv instance, you can register a sentinel on it with `sentinel register` command, just like how you were running it before in the local jsctl session
```bash
@jaseci > sentinel register tesla_ai.jir -set_active true -mode ir
```
After registering, you can then run walker run, just like before in a local jsctl session
```bash
jaseci > walker run talk -ctx "{\"question\": \"I want to schedule a test drive\"}"
```
> **Important**
>
> If this is the first time you are running your jac program on this jsserv instance, you will also need to repeat the actions load commands to load the actions. And for any AI models, use their respective `load_model` action to load the trained models.

And viola! Now you are running your jac program in a jaseci server with jsserv.
The Jaseci server supports a wide range of API endpoints.
All the `jsctl` commands we have used throughput this tutorial have an equivalent API endpoint, such as `walker_run` and `sentinel_register`.
As a matter of fact, the entire development journey in this tutorial can be done completely with a remote jaseci server instance.
You can go to `localhost:8000/docs` to check out all the available APIs.

