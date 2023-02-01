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

## Preparing the `init` walker for production
Up until this point, we have been running our code with just `jac run`.
`jac run` executes the `init` walker of your progarm (analogues to the `__main__` function of python).
Here is what the current `init` walker looks like
```jac
walker init {
    root {
        spawn here ++> graph::tesla_ai;
        spawn here walker::talk;
    }
}
```
It is currently achieving two things.
`spawn here ++> graph::tesla_ai;` initializes the graph and `spawn here walker::talk` run the walker.
This is okay for testing purpose but when actually serving this application, we only need to initialize the graph once.
So remove `spawn here walker::talk` from the init walker before proceeding to the next step.
The init walker should look just contain the graph spawn code, like below:
```jac
walker init {
    root {
        spawn here ++> graph::tesla_ai;
    }
}
```

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
For the purpose of this codelab, we are going to use the following credentials:
```bash
Email: admin@j.org
Password: JaseciAdmin
```

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
In our case, it will be
```bash
jsctl
jaseci > login http://localhost:8000/
Username: admin@j.org
Password: JaseciAdmin
```

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
> Notice the `@` symbol in front of the `@jaseci >` command line prompt. This indicates that your jsctl session is now logged into a jsserv
instance, while `jaseci >` indicates it is in a local session.

While logged into the jsserv instance, you can register a sentinel on it with `sentinel register` command, just like how you were running it before in the local jsctl session
```bash
@jaseci > sentinel register tesla_ai.jir -set_active true -mode ir
```
After registering, you can then run walker run, just like before in a local jsctl session
```bash
@jaseci > walker run talk -ctx "{\"question\": \"I want to schedule a test drive\"}"
```

If this is the first time you are running your jac program on this jsserv instance, this query will not succeed. That is because we need to load the two AI models (bi_enc and tfm_ner) we trained onto the server.
To help you with this, we have provided another jac file `ai_model.jac`.
Find this file in the repo at [this location](https://github.com/Jaseci-Labs/jaseci/blob/main/examples/CanoniCAI/code/ai_model.jac) and put it in your working directory.
Then at the top of your `tesla_ai.jac` import everything with `import {*} with "./ai_model.jac";`.
Note you have modified your jac code since the last time you register with the server sentinel, so in order for the new walkers to be usable, you will need to re-build the jir and register again.
```bash
@jaseci > jac build main.jac
@jaseci > sentinel set -snt active:sentinel -mode ir main.jir
```

> **Note**
>
> Notice the `active:sentinel` syntax. This is an alias. There are many aliases built in with Jaseci that makes it easier to run certain commands. In this case, `active:sentinel` is the alias for the currently active sentinel and is equivalent to typing out the full UUID. If you are curious about what other aliases there are, run `alias list` in jsctl.

To load the previously trained bi-enc model, run
```bash
@jaseci > walker run load_model -ctx "{\"model_type\": \"bi_enc\", \"model_path\": \"YOUR_MODEL_PATH\"}"
```
Similarly, to load the tfm-ner model,
```bash
@jaseci > walker run load_model -ctx "{\"model_type\": \"tfm_ner\", \"model_path\": \"YOUR_MODEL_PATH\"}"
```
> **Note**
>
> Pay attention to the model path. We recommend using absolute path for the model path (e.g. `/home/user/saved_model`). For relative path, the path needs to be relative to the place where the `jsserv runserver` is running in.

Once both models have been loaded, try the talk walker request again
```bash
@jaseci > walker run talk -ctx "{\"question\": \"I want to schedule a test drive\"}"
```

And viola! Now you are running your jac program in a jaseci server with jsserv.
The Jaseci server supports a wide range of API endpoints.
All the `jsctl` commands we have used throughput this tutorial have an equivalent API endpoint, such as `walker_run` and `sentinel_register`.
As a matter of fact, the entire development journey in this tutorial can be done completely with a remote jaseci server instance.
You can go to `localhost:8000/docs` to check out all the available APIs.

> **Note**
>
> `jsserv` is a wrapper around the django `manage.py` script and it supports the commands that `manage.py` supports.

> **Note**
>
> So far we have shown how to run the jaseci server natively on a machine. If you wish to stand up a jaseci server in a kubernetes cluster, you can find an example kubernetes manifest file at https://github.com/Jaseci-Labs/jaseci/blob/main/scripts/jaseci.yaml

## Manage Sentinels on the Jaseci Server
Because we have been running our jac program in a local jsctl environment and under a development setting, we only need to worry about one single user.
In a production setting, our application need to serve many users.
In addition, new accounts will be created when new users sign up for our application.
While it is certainly possible to register a new sentinel for every new user, it is far from ideal from a scalability standpoint.
To solve this, we introduce the concept of the global sentinel.

A global sentinel is a sentinel that is exposed globally and can be set as the active sentinel for any users.
To create a global sentinel, you need to login as a user with admin priviledge so we are going to use the superuser we created earlier.
We are going to first register a sentinel and name it `tesla_ai_global`.
```bash
@jaseci > sentinel register -set_active true -mode ir tesla_ai.jir -name tesla_ai_global
```
To set a sentinel as the global sentinel for the jaseci server, we run
```bash
@jaseci > global sentinel set -snt sentinel:tesla_ai_global
```
Now that this sentinel is the global sentinel, to activate this sentinel as the active sentinel for any given user, run the following while logged in as the user
```bash
@jaseci > sentinel active global
```
This will set the active sentinel for the user to the global sentinel, which in our case is named `tesla_ai_global`.
Once this is set, any future walker run requests will by default use the global sentinel.

To update the global sentinel, run as the admin user
```bash
@jaseci > sentinel set -snt sentinel:tesla_ai_global -mode ir tesla_ai.jir
```
This will update the gloabl sentinel with the updated `jir` code and because this is a global sentinel, any users that have the global sentinel set as their active sentinel will also effectively be running with an updated sentinel.

## Manage Graphs
Now that we have the global sentinel set up, it's time to discuss the management of graphs in a production environment.
Let's first create two general categories of application, un-authenticated and authenticated applications.
Un-authenticated applications do not require any user authentication and can be used by anyone in the world as long as they access the URL of the application.
This category of applications usually serve functions that can benefit a wide range of audience but lack any personalized usage due to lack of access to personal data that is only possible with authentication.
Example of un-authenticated applications include chatbot that provides public service annoucement or information that are useful to the general public.
In contrast, authenticated applications require user to log in first before they can use the application.
The application then can fetch information and data specific to the user that is interacting with the application.
Example of authenticated applications include a virtual assistant within your bank app that you can use about your account balance or your recent account transactions.

Both un-authenticated and authenticated applications can utilize the global sentinel pattern.
Developers of the application register and update a global sentinel for all users.
On the other hand, depending on the application, the management of graphs can be different.
For un-authenticated applications, the front-end of the application is often integrated with the backend with a service account.
All users will be effectively using the graph of this service account.
For authenticated applications, each user will often have a corresponding account in the jaseci backend and their own graph.
Therefore, a graph needs to be created and set as active for every new user creation. To create a graph, run
```bash
@jaseci > graph create -set_active true
```
And depending on the application, you might also need to initialize the graph with the init walker
```bash
@jaseci > walker run init
```
> **Note**
>
> Our tesla bot falls into the category of un-authenticated applications. Anyone can ask about FAQs and schedule a test drive. So for this tutorial, we will use the admin account as our service account and its graph as the active graph

## The Jaseci RESTful APIs
With a jaseci web server (i.e., `jsserv`), we also get access to the full suite of Jaseci RESTful APIs.
You can go to `http://localhost:8000/docs/` to checkout the list of available APIs and their documentation and request and response payload format.
The documentation looks like this

![](../images/api_docs.png)
Every `jsctl` command has a corresponding API endpoint.
Click on the triangle to the right of the endpoint to see details on its request and response format.
The command line argument to the `jsctl` command becomes the fields in the request payload of the API endpoint.
`jsctl` is great for rapid development and testing but for deploying a jaseci application to production, a set of RESTful API endpoints is the industry standard.
Here are the most commonly used endpoints that you should pick up and get familarized first.
* `/user/create` to create a new user
![](../images/api_docs_user_create.png)
* `/js/sentinel_register` to register a sentinel
![](../images/api_docs_sentinel_register.png)
* `/js/walker_run` to run a walker
![](../images/api_docs_walker_run.png)

## Integration with a Webapp
We are now going to show an example of how to integrate with a frontend to our tesla chatbot.
We have provided a template web-based frontend at https://github.com/Jaseci-Labs/jaseci/blob/main/examples/CanoniCAI/code/html/.
This is a simple chatbot frontend that supports both voice and text input.
It also coverts the response text to speech and speak it back.

Here is a screenshot of the UI. You can click on the microphone button to talk to it or use the textbox below for a text input.
![](../images/web_ui.png)

The web frontend communciates with the Jaseci backend via HTTP requests.
Here is the relevant code where the frontend makes a POST request to the `/js/walker_run` API to run the `talk` walker to ask a question.
```js
const getAnswer = async (question) => {
      let data = {
        ctx: { "question": question },
        name: "talk"
      }

      try {
        // NOTE: Change this URL to your Jaseci server URL.
        // NOTE: Change the token to your authenticated token
        let result = await fetch('http://localhost:8000/js/walker_run', {
          method: 'POST',
          mode: 'cors',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'token bf6c3138799af356cbec27da90de0f7476fd9e25059c83dc0dfdd339ff68dd5b'
          },
          body: JSON.stringify(data),
        })
        result = await result.json();

        const answer = result.report[0];

        document.querySelector('#answer').innerHTML = answer;
        speech.text = answer.replace(/https?.*?(?= |$)/g, "");
        var voices = window.speechSynthesis.getVoices();
        speech.voice = voices[7];
        speechSynthesis.getVoices().forEach(function (voice) {
          console.log(voice.name, voice.default ? voice.default : '');
        });

        // Start Speaking
        window.speechSynthesis.speak(speech);

      } catch (error) {
        console.log(error)
      }
    }
```
Let's quickly dissect this API call.
* It is sending a POST request, as specified by the `method` field.
* It is sending the request to the URL `http://localhost:8000/js/walker_run`. You should replace the `localhost:8000` with your own jaseci server URL.
* The request payload is a JSON data structured stored in `data`, as follows. The `name` field specifies the name of the walker to run and `ctx` is a dictionary containing all neccessary parameters to the walker, just like what we have been doing with `walker run` in `jsctl`. In this webapp, the question is being pulled from the frontend from either the Speech-to-text engine or the text input.
```json
{
    "ctx": {
        "question": "USER QUESTION",
    },
    "name": "talk"
}
```
> **Note**
>
> You need to update the webapp to point to your own jaseci server URL (line 360 of `index.html`) as well as an updated authentication token (line 365 of `index.html`) which can you obtain from logging in via `jsctl`.
