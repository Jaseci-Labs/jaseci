# Request Action Library

How to use the built in requests action library to make outgoing API calls from Jac to 3rd party API's.

## Introduction
First of all there are 4 types of request actions in jaseci, they are as follows:
* POST
* GET
* PUT
* DELETE

There are three standard parameters for each requests and they are as follows:
* url (string): the url where you will make the request
* data (dict): the information that is required to pass in the request
* header (dict): this will be the header information for the request

## GET

GET is used to request data from a specified resource.

```
request.get(url, data, headers);
```

## POST

POST is used to send data to a specified resource.

```
request.post(url, data, headers);
```


## PUT

PUT is used to update data from a specified resource.

```
request.put(url, data, headers);
```

## DELETE 

DELETE is used to delete data from a specified resource.

```
request.delete(url, data, headers);
```

## EXAMPLE

So let's create a quick SIMPLE RESTFUL application example (TODO) from JSON PlACEHOLDER and you can add this to CanoniCAI and use it.

```
walker get_todo {
    has uid;
    has title;
    has completed = false;
    
    has url = "https://jsonplaceholder.typicode.com/todos/1";
    has headers = {};

    report request.get(url, {}, headers);
}

walker post_todo {
    has uid;
    has title;
    has completed = false;
    
    has url = "https://jsonplaceholder.typicode.com/todos/";
    has headers = {};
    
    report request.post(url, {"userId": uid, "title": title, "completed": completed}, headers);
}

walker put_todo {
    has uid;
    has title;
    has completed = false;
    
    has url = "https://jsonplaceholder.typicode.com/todos/1";
    has headers = {};


    report request.put(url, {"userId": uid, "title": title, "completed": completed}, headers);
}

walker delete_todo {
    has uid;
    has title;
    has completed = false;
    
    has url = "https://jsonplaceholder.typicode.com/todos/1";
    has headers = {};

    report request.delete(url, {}, headers);
}
```

Let's test the application we build, create a file name **api.jac** and copy over all the code to the file. Great let's run each walker.

First let's run get_todo walker:
* jac run api.jac -walk get_todo

Let's see the result: 
```
jaseci > jac run api.jac -walk get_todo  
{
  "success": true,
  "report": [
    {
      "status_code": 200,
      "response": {
        "userId": 1,
        "id": 1,
        "title": "delectus aut autem",
        "completed": false
      }
    }
  ],
  "final_node": "urn:uuid:12a5affa-c0a2-4959-9e3d-54e3f4cd4ca1",
  "yielded": false
}
```

post_todo walker:
* jac run api.jac -walk post_todo
```
jaseci > jac run api.jac -walk post_todo
{
  "success": true,
  "report": [
    {
      "status_code": 201,
      "response": {
        "userId": null,
        "title": null,
        "completed": false,
        "id": 201
      }
    }
  ],
  "final_node": "urn:uuid:eaca3dfa-3abc-4c03-9d55-d2e5cdf1b1e6",
  "yielded": false
}
```

put_todo walker:
* jac run api.jac -walk put_todo -ctx "{\"id\": 201, \"title\":\"hi\"}" 

```
jaseci > jac run api.jac -walk put_todo -ctx "{\"id\": 201, \"title\":\"hi\"}" 
{
  "success": true,
  "report": [
    {
      "status_code": 200,
      "response": {
        "userId": null,
        "title": "hi",
        "completed": false,
        "id": 1
      }
    }
  ],
  "final_node": "urn:uuid:393a0094-57d5-4745-944d-9fac007edc38",
  "yielded": false
}
```

delete_todo walker:
* jac run api.jac -walk delete_todo

```
jaseci > jac run api.jac -walk delete_todo
{
  "success": true,
  "report": [
    {
      "status_code": 200,
      "response": {}
    }
  ],
  "final_node": "urn:uuid:6f90aac5-7284-48c7-b5df-1abc64dfdf10",
  "yielded": false
}
```

So now everything is working. You can now implement this setup to your code implementation and have fun.

All you have to do now is build and set the sentinel and call these walker and you will be able to use the functionality.

