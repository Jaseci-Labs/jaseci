# Setting Up Your Jac Cloud Application (Part 1/3)
Jac Cloud is a jaclang plugin that bootstraps your jac application into a running web server. It allows you to serve your jac code as a REST API and interact with it from any client that can make HTTP requests. To set up Jac Cloud, you need to install the `jaclang` and `jac-cloud` python package using pip:

```bash
pip install jaclang==0.7.19 jac-cloud==0.1.1
```

## Installing your VSCode Extension
To make your development experience easier, you should install the jac extension for Visual Studio Code. This extension provides syntax highlighting, code snippets, and other features to help you write Jac Cloud code more efficiently. You can install the extension from the Visual Studio Code marketplace [here](https://marketplace.visualstudio.com/items?itemName=jaseci-labs.jaclang-extension).

![Jac Extension](images/1_vscode.png)

## Your First Jac Cloud Application
Now that you have your database set up, you can start building your first Jac application. Create a new file called `server.jac` and add the following code:

```jac
walker interact {
    can return_message with `root entry {
        report {
            "response": "Hello, world!"
        };
    }
}

walker interact_with_body {
    has name: str;

    can return_message with `root entry {
        report {
            "response": "Hello, " + self.name + "!"
        };
    }
}
```

This code defines two walkers, `hello_world_no_body` and `hello_world_with_body`. The `hello_world_no_body` walker returns a simple message "Hello, world!" when called. The `hello_world_with_body` walker takes a `name` parameter and returns a message "Hello, `name`!". No need to worry about what a walker is for now. Think of it as a function that can be called as an API endpoint.

Now, let's serve this code using Jac Cloud by running the following command:

```bash
jac serve server.jac
```

This command starts the Jac Cloud server. The server will serve the code in `server.jac` as an API. You can now access the API at `http://localhost:8000`. Go to `http://localhost:8000/docs` to see the Swagger documentation for the API. It should look something like this:

![Swagger Docs](images/1_swagger.png)

Now, before we can fully test the API, it is important to know that by default, Jac Cloud requires authentication to access the API. So we need to create a user and get an access token to access the API. You can do this using the Swagger UI or by making HTTP requests. We will show you how to do this using HTTP requests.

For this tutorial, we use `curl` to send API requests. You can also use tools like Postman or Insomnia to faciliate this.

Keep the previous terminal with the `jac serve` process running and open a new terminal. In the new termminal, run the following command to register a new user with the email `test@gmail.com` and password `password`.

```bash
curl --location 'http://localhost:8000/user/register' \
--header 'Content-Type: application/json' \
--header 'Accept: application/json' \
--data '{
  "password": "password",
  "email": "test@mail.com"
}'
```

We should see
```json
{"message":"Successfully Registered!"}
```

Next, we'll need to login and get the access token. To do this, run the following command:

```bash
curl --location 'http://localhost:8000/user/login' \
--header 'Content-Type: application/json' \
--header 'Accept: application/json' \
--data '{
  "password": "password",
  "email": "test@mail.com"
}'
```

We should see a response similar to this:

```json
{"token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY2ZGYzN2Y0MjIzNDM2N2QxZDMzMDE1MSIsImVtYWlsIjoidGVzdEBtYWlsLmNvbSIsInJvb3RfaWQiOiI2NmRmMzdmNDIyMzQzNjdkMWQzMzAxNTAiLCJpc19hY3RpdmF0ZWQiOnRydWUsImV4cGlyYXRpb24iOjE3MjYwMzAyNDUsInN0YXRlIjoiZGlCQnJOMHMifQ.oFQ5DuUBwzGVedmk4ktesFIelZR0JH8xx7zU4L_Vu3k","user":{"id":"66df37f42234367d1d330151","email":"test@mail.com","root_id":"66df37f42234367d1d330150","is_activated":true,"expiration":1726030245,"state":"diBBrN0s"}}
```

Save the `token` value. This will be our access token to authenticate with the API for subsequen requests.

Let's now test the `interact` API we created earlier:
```bash
curl -X POST http://localhost:8000/walker/interact -H "Authorization: Bearer <TOKEN>"
```

Replace `<TOKEN>` with the access token you received. This command will return the message "Hello, world!".

```json
{"status":200,"reports":[{"response":"Hello, world!"}]}
```

You can also do this in the browser by visiting the Swagger docs `http://localhost:8000/docs` and adding the `Authorization` header with the value `Bearer ACCESS TOKEN`.

That's it! You have successfully set up your Jac application and served your first API. In the [next](2_building-a-rag-chatbot.md) part we will learn how to build a simple conversational agent using Jac.