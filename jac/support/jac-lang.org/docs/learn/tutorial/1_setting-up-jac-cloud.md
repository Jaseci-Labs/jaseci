# Setting Up Your Jac Cloud Application (Part 1/3)
Jac Cloud is a jaclang plugin that bootstraps your jac application into a running web server. It allows you to serve your jac code as a REST API and interact with it from any client that can make HTTP requests. To set up Jac Cloud, you need to install the `jaclang` and `jac-cloud` python package using pip:

```bash
pip install jaclang==0.7.19 jac-cloud==0.1.1
```

## Setting Up Your Database
Like most API servers, jac-cloud requires a database to store data persistently. Jac-cloud uses mongoDB as the database engine. You will need to have a running mongodb service. You can do this in several ways:

- Setup MongoDB manually on your local maching
- Using a container service like docker
- Using a free cloud service like [MongoDB Atlas](https://www.mongodb.com/products/platform/atlas-database).

In this tutorial we will show you how to do this manually and also using Docker (recommended).

### Running a Mongodb Replica Set Locally
To set up a mongodb replica set, follow these steps:

- Running a mongoDB replica set locally.
    - mongoDB community edition is free to use and run locally. Follow the installation and starting instructions from the mongoDB documentation [here](https://www.mongodb.com/docs/manual/installation/). Select the right one based on your OS.
    - After installing, start the mongoDB service by running the following command:
    ```bash
    mongod --dbpath DB_DATA_PATH --replSet my-rs
    ```
    Replace `DB_DATA_PATH` with the path to your database data directory. It can be any directory. It will be used to store the files for the database. This will start the mongoDB service with a replica set named `my-rs`.
    - **First time only**: The first time you start the mongodb, do the following two quick steps
        - Run the command `mongosh` in another terminal to open the mongo shell.
        - In the mongo shell, run the following command to initiate the replica set:
        ```bash
        rs.initiate()
        ```
        This command will initiate the replica set with the default configuration. You can customize the configuration as needed.
        - Run `Exit` to exit the mongo shell.

### Running a Mongodb Replica Set using Docker
To set up a mongodb replica set using Docker, follow these steps:

- Ensure you have Docker installed on your machine. You can download and install Docker from the official website [here](https://www.docker.com/products/docker-desktop).
- Pull the mongoDB image from Docker Hub:
```bash
docker pull mongodb/mongodb-community-server:latest
```
- Run the image as a container:
```bash
docker run --name mongodb -p 27017:27017 -d mongodb/mongodb-community-server:latest --replSet my-rs
```
This command will start a mongoDB container with the name `mongodb` and expose port `27017` to the host machine.

To check that the docker is up and running, run `docker ps` to get the lists of running container and you should see the following:
```
CONTAINER ID   IMAGE                                     COMMAND                  CREATED          STATUS              PORTS                       NAMES
d289c01c3f1c   mongodb/mongodb-community-server:latest   "python3 /usr/local/…"   12 seconds ago   Up 11 seconds       0.0.0.0:27017->27017/tcp    mongodb
```
- Install the mongo shell to connect to the mongoDB container. You can install the mongo shell by following the instructions [here](https://www.mongodb.com/docs/mongodb-shell/install/).
- Connect to the MongoDB Deployment with mongosh
```bash
mongosh --port 27017
```
- **First time only**: The first time you start the mongodb, do the following two quick steps
    - Run the command `mongosh` in another terminal to open the mongo shell.
    - In the mongo shell, run the following command to initiate the replica set. This command will initiate the replica set with the default configuration. Feel free to learn more about mongodb replica set [here](https://docs.mongodb.com/manual/tutorial/deploy-replica-set/).
    ```bash
    rs.initiate({_id: "my-rs", members: [{_id: 0, host: "localhost"}]})
    ```
    We should see the following output:
    ```
    { ok: 1 }
    ```
    - Run `exit` to exit the mongo shell.

You have successfully set up a running MongoDB service our application can use as the database.

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

This code defines two walkers: `interact` and `interact_with_body`. The `interact` walker returns a simple message "Hello, world!" when called. The `interact_with_body` walker takes a `name` parameter and returns a message "Hello, `name`!".
You don't need to worry about what a walker is for now. Just think of it as a function that can be called as an API endpoint.

Now, let's serve this code using Jac Cloud by running the following command:

```bash
DATABASE_HOST=mongodb://localhost:27017/?replicaSet=my-rs jac serve server.jac
```

This command starts the Jac Cloud server with the database host set to `mongodb://localhost:27017/?replicaSet=my-rs`. The server will serve the code in `server.jac` as an API. You can now access the API at `http://localhost:8000`. Go to `http://localhost:8000/docs` to see the Swagger documentation for the API. It should look something like this:

![Swagger Docs](images/1_swagger.png)

Now, before we can fully test the API, it is important to know that by default, Jac Cloud requires authentication to access the API. So we need to create a user and get an access token to access the API. You can do this using the Swagger UI or by making HTTP requests. We will show you how to do this using HTTP requests.

For this tutorial, we use `curl` to send API requests. You can also use tools like [Postman](https://www.postman.com/downloads/) or [Insomnia](https://insomnia.rest/product/automated-testing) to faciliate this.

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