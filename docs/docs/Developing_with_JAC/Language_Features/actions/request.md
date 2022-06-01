---
title :  Request Actions
---

Jaseci allows for in-code use of common  request methods.
### Get Request
```jac 
# make get request 
# url : string  - url to where the request will be made 
# data : dictionary - data being sent that will be converetd to json.
# header : dicionary -  header data 
response = request.get(url ,data , headers)
```
### Post Request
```jac 
# make post request 
# url : string  - url to where the request will be made 
# data : dictionary - data being sent that will be converetd to json.
# header : dicionary -  header data 
response = request.post(url ,data , headers)
```
### Put Request
```jac 
# make put request 
# url : string  - url to where the request will be made 
# data : dictionary - data being sent that will be converetd to json.
# header : dicionary -  header data 
response = request.put(url ,data , headers)
```

### Delete Request
```jac 
# make delete request 
# url : string  - url to where the request will be made 
# data : dictionary - data being sent that will be converetd to json.
# header : dicionary -  header data 
response = request.delete(url ,data , headers)
```

### Head Request
```jac 
# make head request , returns header of  a get request alone
# url : string  - url to where the request will be made 
# data : dictionary - data being sent that will be converetd to json.
# header : dicionary -  header data 
response = request.head(url ,data , headers)
```

### Option Request 
```jac 
# make options request , requests permitted communications options fror a given url or server.
# url : string  - url to where the request will be made 
# data : dictionary - data being sent that will be converetd to json.
# header : dicionary -  header data 
response = request.get(url ,data , headers)
```

### File upload
```jac 
# used to upload a file or files
# url : string  - url to where the request will be made 
# file : single base64 encoded file
# files : list of base64 encode files.
# header : dicionary -  header data 
response = request.multipart_base64(url ,file , headers)
```

### Download File
```jac
# url : string  - url to where the request will be made 
# header : dicionary -  header data 
# encoding : strign - file format , default is utf-8
downloaded_file = request.file_download_base64(url,header,encoding)

```