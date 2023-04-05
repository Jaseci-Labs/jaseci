# Request Actions Library

- [Request Actions Library](#request-actions-library)
    - [Get Request](#get-request)
    - [Post Request](#post-request)
    - [Put Request](#put-request)
    - [Delete Request](#delete-request)
    - [Head Request](#head-request)
    - [Option Request](#option-request)
    - [File upload](#file-upload)
    - [Download File](#download-file)

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