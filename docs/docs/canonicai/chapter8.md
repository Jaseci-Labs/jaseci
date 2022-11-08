# Request Action Library

In this tutorial, you are going to learn how to use the built in requests action library to make outgoing API calls from Jac to 3rd party API's.

Excited? Hell yeah! Let's jump in.

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

So let's create a quick SIMPLE RESTFUL application example (TODO) and you can add this to CanoniCAI and use it.

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

All you have to do now is build and set the sentinel and call these walker and you will be able to use the functionality.

