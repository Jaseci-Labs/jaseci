---
sidebar_position: 3
---

# Setting up Jaseci Server

Jaseci Serv allows for the development of APIs to interact with your JAC Program.

**Step 1:**

Install Jaseci-Serv*
```
pip install jaseci-serv
```

let's open a new terminal in our working directory and run :

**Step 2:**
```
jsserv makemigrations base
```
This will create a database that will be used to run a jaseci instance of our application. It creates a mydatabase file in your working directory.

**Step 3:**

Install the Schema and Database.

```
jsserv migrate
```

**Step 4:**

Start the server

```
jsserv runserver 0.0.0.0:8000
```
This will start your Jaseci Server to run your application. Visit localhost:8000 .

Let's now spawn 2 new terminal in our current working directory.

**Step 5:**
In new terminal 1

Create an account for the server.
```
jsserv createsuperuser
```
You will be prompted to enter an email and password.

In new  terminal 2

**Step 6:**
Start jsctl. Run :
```
jsctl
```

**Step 7:**
Login to Jaseci Shell
```
login http://localhost:8000
```
login with the credientals used to create the super user earlier.

In new terminal 1 :

**Step 8:**
Compile Jac program to JIR bit

```
jsctl jac build main.jac
```

**Step 9:**
Register a new Sentinel :

```
sentinel register -name main -mode ir main.jir
```

**Step 10:**
To show the entities in the code run :
```
alias list
```
Copy the sentinel ID , we will need it.


**Step 11:**

Open up Postman

* Grab a token from Jaseci that represents an active session of the super user. Make a Post request to user/token
* Body of the request is as follows:

```
{
"email" : "email@gmail",
"password" : "passsowrd"
}
```

* Copy token returned. Add it to the authorization header with the word "token" added before

You can now make API calls to your JAC program.
