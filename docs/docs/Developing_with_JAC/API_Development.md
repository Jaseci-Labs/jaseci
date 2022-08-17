---
sidebar_position: 5
---

# API Development

# Overview 
JAC programs can be transformed to have fully functional APIs. This is done with the help of the `jaseci-serv` package. You will be able to expose your JAseci Program to API calls in order to operate the same way when you use the command line to enter your responses.

### Installing Jaseci Server
jaseci servver can be installed as a pip package . Run the following to install :
```
pip install jaseci-serv
```

### Setting up your Dev Server

#### Running your Dev Server

The Dev Server can be easily started up with a single command but before we do we need to establish a database for out program. 
Run the following in the root directory of your main file. This will create a mydatabase.db file in your directory.

```
jsserv makemigrations base
```
Then run this next command to install the schema and Database for your JAC program. Run: 
```
jsserv migrate
```
Now start up your server by running :
```
jsserv runserver 0.0.0.0:8000
```
#### Creating a Super User

To make calls to the API you will need to create a super user account. To do this run the following and enter a email and password :
```
jsserv createsuperuser
```
#### Logging in to Jaseci

Open a new terminal and start the jsctl terminal by running :
```
jsctl
```
Log in to your Dev Server by running and enter your super user infromation from earlier :
```
login http://localhost:8000
```

## JAC I/O for APIs

### Outputting your payload 

To return a response to Walkers when calls are made we need to use the report key word in the JAC program.
Report will return all the information  below when calls are made .
```jac 
 report {"message": message, "utterance": utterance, "intent": chosen_intent, "scores": qa_scores, "node": nodeobj};
 ```

### Input with Walker variables
Walker variables can be set using API calls. In the walker ,talker is has a variable named utterance. when we make an API call we can pass the name of variable and a value in to the `ctx` field of the POST request json.

The `ctx` field has the name of the variable and the value to be sent to the walker.
```
{
    "name" :"talker", # name of walker to be called
    "nd": "urn:uuid:f7153e9d-739d-4427-b93e-570f84ce560f", # node walker will be set to, if not included will go to the main node.
    "ctx" : {"utterance":"one pager website "}, # information sent to the walker
    "snt" : "urn:uuid:8da9ffaa-0cec-4f01-a4a0-5084be2c1fee", #sentinel ID  of the program 
    "detailed" : "false" # returns additional information for the walker
}
```
Walker talker will ow have it's variable set to the value sent in the POST request.

```jac
walker talker {
    
    has utterance = "";
 

    Node_state {

        if(!utterance) {
            
            report {"message" :"No utterance set"}
            } else {
                report {"message":"Utteracne has been set"}
            }
```

### Sending Status code

Status code can be returned using the same report function. 

```jac
report : status = statusCode

```
### Logging Errors 
To log errors we use the standar JAseci action `std.err()`

```
std.err()

```

## Running you JAC program on your Dev Server

### Compiling your JAC code.
When we compile our JAC code we change to a JIR bit file. This is what will be used to create the Sentinel, our living JAC code.
```
jsctl jac build main.jac

```
### Registering a Sentinel
The registering sentinel is to make the JIR bit file accessible via API calls. In the directory of your main.jir file , run :

```
sentinel register -name main -mode ir main.jir
```

### Consuming your API
Your APis are now avaliable to make calls to. See `http://localhost:8000/docs` to see all the endpoints you can use.

Make a  request to  Dev Server to retrieve the user token. The user token grants access to make API calls to your JAC program to retrieve the token make a request to `http://localhost:8000/user/token/` .The body of the request will be the following :

```
{
    "name" : "email@domain.com", # email of superuser created earlier
    "password" : "password" # password of useruser created earlier
}
```



### Using Postman 


In Postman add  in to the header section  the word "token" followed by space then the actual  token retrieved.

You can now make POST request to the exposed APIs of your JAC program.


### Calling your Walkers

You will make API calls to the walker  you specify. To make calls to your walker you will send your request to this endpoint : `http://localhost:8000/js/walker_run` . 



Post request to the walker will be in this format :
```
{
    "name" :"talker", # name of walker to be called
    "nd": "urn:uuid:f7153e9d-739d-4427-b93e-570f84ce560f", # node walker will be set to, if not included will go to the root node.
    "ctx" : {"utterance":"one pager website "}, # information sent to the walker
    "snt" : "urn:uuid:8da9ffaa-0cec-4f01-a4a0-5084be2c1fee", #sentinel ID  of the program 
    "detailed" : "false" # returns additional information for the walker
}
```

### Getting Graph Data



