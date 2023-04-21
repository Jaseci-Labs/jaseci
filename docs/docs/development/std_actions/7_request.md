# Request Actions Library

Jaseci allows for in-code use of common  request methods.

### Get Request

Make get request
`url` : `string`  - url to where the request will be made
`data` : `dictionary` - data being sent that will be converetd to json.
`header` : `dicionary` -  header data

```jac
response = request.get(url ,data , headers);
```

### Post Request

Make post request.

`url` : `string` - url to where the request will be made
`data` : `dictionary` - data being sent that will be converetd to json.
`header` : `dicionary` -  header data

```jac
response = request.post(url ,data , headers);
```
### Put Request

Make put request
`url` : `string`  - url to where the request will be made
`data` : `dictionary` - data being sent that will be converetd to json.
`header` : `dicionary` -  header data

```jac
response = request.put(url ,data , headers);
```

### Delete Request

Make delete request.

`url` : `string`  - url to where the request will be made
`data` : `dictionary` - data being sent that will be converetd to json.
`header` : `dicionary` -  header data

```jac
response = request.delete(url ,data , headers);
```

### Head Request

Make head request , returns header of  a get request alone.
`url` : `string`  - url to where the request will be made.
`data` : `dictionary` - data being sent that will be converetd to json.
`header` : `dicionary` -  header data.

```jac
response = request.head(url ,data , headers);
```

### Option Request

Make options request , requests permitted communications options fror a given url or server.

`url` : `string`  - url to where the request will be made
`data` : `dictionary` - data being sent that will be converetd to json.
`header` : `dicionary` -  header data

```jac
response = request.get(url ,data , headers);
```

### File upload

Used to upload a file or files
`url` : `string`  - url to where the request will be made
`file` : `single` base64 encoded file
`files` : `list` of base64 encode files.
`header` : `dicionary` -  header data

```jac
response = request.multipart_base64(url ,file , headers);
```

### Download File

`url` : `string`  - url to where the request will be made
`header` : `dicionary` -  header data
`encoding` : `string` - file format , default is utf-8

```jac
downloaded_file = request.file_download_base64(url,header,encoding);
```
### An example Jac Application using the Requests Library

So let's create a quick SIMPLE RESTFUL application example, a ToDo list app.
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

