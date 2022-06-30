Visit jaseci.org for more info!

---
---

# **How to upload file**

## **Old approach:** (still supported)

Most of the requests uses json as request body. This will have some limitations if you want to include file thru json.

## **Structure**:

```json
// Sample Request
{
    "name": "walker_name",
    "ctx": {
        "anyFieldNameForYourFile": [{
            "name": "sample.txt",
            "base64": "MAo=" // "MAo=" is equivalent to "0\n"
        }]
    },
    "nd": "active:graph",
    "snt": "active:sentinel"
}
```

## **Note**:

`anyFieldNameForYourFile` structure is based on jaseci action `request.multipart_base64`.
You can use different structure. However, you will still need to request it as base64. You will also need to reconstruct it to `request.multipart_base64`'s files structure if you want to pass it on different service (internal or 3rd party) using `multipart/form-data`

```json
// request.multipart_base64's files parameter structure
[
    {

        "field": "anyFieldName", // Optional: Default is "file"
        "name": "sample.txt",
        "base64": "MAo="
    }
]
```

## **Limitation**

> Each Base64 digit represents exactly 6 bits of data. So, three 8-bits bytes of the input string/binary file (3×8 bits = 24 bits) can be represented by four 6-bit Base64 digits (4×6 = 24 bits).
>
> This means that the Base64 version of a string or file will be at least 133% the size of its source (a ~33% increase). The increase may be larger if the encoded data is small. For example, the string "a" with length === 1 gets encoded to "YQ==" with length === 4 — a 300% increase.

Some server/service have limit in terms of accepting request. For example, your file is 4MB and you converted it to base64, some server will return `413: Payload Too Large`. This may also affect upload time since it will add some additional file size.

To improve developer/user experience, we support multipart/form-data approach

---

# **How to upload file using `multipart/form-data`**

## **What is `multipart/form-data`**

> The enctype attribute specifies how the form-data should be encoded when submitting it to the server. Multipart/form-data is one of the most used enctype/content type.
In multipart, each of the field to be sent has its content type, file name and data separated by boundary from other field.
>
> No encoding of the data is necessary, because of the unique boundary. The binary data is sent as it is. The server reads the until the next boundary string.


## **Definition of `multipart/form-data`**

> The media-type multipart/form-data follows the rules of all multipart MIME data streams as outlined in [RFC 2046]. In forms, there are a series of fields to be supplied by the user who fills out the form. Each field has a name. Within a given form, the names are unique.
>
> “multipart/form-data” contains a series of parts. Each part is expected to contain a content-disposition header [RFC 2183] where the disposition type is “form-data”, and where the disposition contains an (additional) parameter of “name”, where the value of that parameter is the original field name in the form. For example, a part might contain a header:
>
> Content-Disposition: form-data; name=”user”
with the value corresponding to the entry of the “user” field.
>
> Field names originally in non-ASCII character sets may be encoded within the value of the “name” parameter using the standard method described in RFC 2047. As with all multipart MIME types, each part has an optional “Content-Type”, which defaults to text/plain.
>
> If the contents of a file are returned via filling out a form, then the file input is identified as the appropriate media type, if known, or “application/octet-stream”.
>
> If multiple files are to be returned as the result of a single form entry, they should be represented as a “multipart/mixed” part embedded within the “multipart/form-data”.
Each part may be encoded and the “content-transfer-encoding” header supplied if the value of that part does not conform to the default encoding.

## **Implementation**

Request using `application/json`

```json
Request:
URL: http://localhost:8000/js/walker_run?testQueryField=1
Method: POST

{
	"name": "walker_name",
	"nd": "active:graph",
	"snt": "active:sentinel",
	"ctx": {
        "yourCtxField1": "value1",
        "yourCtxField2": "value2",
        "yourCtxField3": "value3",
        "fileTypeField": [
            {
				"name": "test.txt",
				"base64": "MAo="
			}
        ],
        "fileTypeSameField": [
            {
				"name": "test.txt",
				"base64": "MAo="
			}
        ]
    },
    "additionalFIeld": 1
}
```

Request using `multipart/form-data`

![Insomnia: multipart/form-data](https://user-images.githubusercontent.com/74129725/170541725-e82822b7-12e5-4a60-99b5-5136c6cfc0ae.png)

Curl equivalent of `multipart/form-data`
```bash
curl --request POST \
  --url http://localhost:8000/js/walker_run?testQueryField=1 \
  --header 'Authorization: token {yourToken}' \
  --header 'Content-Type: multipart/form-data' \
  --form name=walker_name \
  --form nd=active:graph \
  --form snt=active:sentinel \
  --form 'ctx=path/to/file/context.json' \
  --form 'fileTypeField=path/to/file/test.txt' \
  --form 'fileTypeSameField=path/to/file/test.txt' \
  --form 'fileTypeSameField=path/to/file/test.txt'
  --form snt=active:sentinel \
```

`context.json`
```json
{
    "yourCtxField1": "value1",
    "yourCtxField2": "value2",
    "yourCtxField3": "value3"
}

```

`test.txt`
```
 0

```

## **Advantages**
 - request with multiple part with different content-type is supported
 - files are not subjected for additional size like base64 does
 - it will also avoid `413: Payload Too Large` since it will use `multipart/form-data` as main request Content-Type instead of `application/json`
 - File handling can now be improved in terms of performance since `application/json` request will always saved in memory while `multipart/form-data` can be on memory or on disk. (On disk handling will be for future improvements)
 - You can also access the files using `has fieldName` excluding `ctx`

---
---

# **Walker Callback**

Walker callback is used for running a walker to a specific node using `public key` instead of authorization token.

## **Use Case**
Generating public URL that can be used as callback API for 3rd party Webhook API.
You may also use this as a public endpoint just to run a specific walker to a specific node.

## **Structure**

**POST** /js_public/walker_callback/`{node uuid}`/`{spawned walker uuid}`?key=`{public key}`

## **Step to Generate**

### **1. Jac Code**

```js
walker sample_walker: anyone {
    has fieldOne;
    with entry {
        report 1;
    }
}
```

### **2. Register Sentinel**

```bash
curl --request POST \
  --url http://localhost:8000/js/sentinel_register \
  --header 'Authorization: token {yourToken}' \
  --header 'Content-Type: application/json' \
  --data '{ "name": "sentinel1", "code": "walker sample_walker: anyone {\r\n\thas fieldOne;\r\n\twith entry {\r\n\t\treport 1;\r\n\t}\r\n}" }'
```
```json
// RESPONSE
[
	{
		"version": "3.5.7",
		"name": "zsb",
		"kind": "generic",
		"jid": "urn:uuid:b4786c7a-cf24-49a4-8c2c-755c75a35043",
		"j_timestamp": "2022-05-11T05:57:07.849673",
		"j_type": "sentinel"
	}
]
```

### **3. Spawn Public Walker** (sample_walker)

```bash
curl --request POST \
  --url http://localhost:8000/js/walker_spawn_create \
  --header 'Authorization: token {yourToken}' \
  --header 'Content-Type: application/json' \
  --data '{ "name": "sample_walker", "snt":"active:sentinel" }'
```
```json
// RESPONSE
{
	"context": {},
	"anchor": null,
	"name": "sample_walker",
	"kind": "walker",
	// this is the spawned walker uuid to be used
	"jid": "urn:uuid:2cf6d0dc-e7eb-4fc8-8564-1bbdb48baad3",
	"j_timestamp": "2022-06-07T09:45:22.101017",
	"j_type": "walker"
}
```

### **4. Getting Public Key**

```bash
curl --request POST \
  --url http://localhost:8000/js/walker_get \
  --header 'Authorization: token {yourToken}' \
  --header 'Content-Type: application/json' \
  --data '{ "mode": "keys", "wlk": "spawned:walker:sample_walker", "detailed": false }'
```
```json
// RESPONSE
{
	// this is the public key used for walker callback
	"anyone": "97ca941e6bf1f43c3a4e531e40b2ad5a"
}
```

### **5. Construct the URL**
*Assuming there's a node with uuid of `aa1bb26e-238b-40a0-8e39-333ec363ace7`*
*this endpoint can now be accessible by anyone*

>**POST** /js_public/walker_callback/`aa1bb26e-238b-40a0-8e39-333ec363ace7`/`2cf6d0dc-e7eb-4fc8-8564-1bbdb48baad3`?key=`97ca941e6bf1f43c3a4e531e40b2ad5a`

---
---

# **Global Reference Syntax** (to be improve)

This for accessing current thread attributes.

## **`global.context` \<Dict\>**

It will return global variables

## **`global.info` \<Dict\>**
 - report
 - report_status
 - report_custom
 - request_context
 - runtime_errors

> **global.info[`"report"`]**
>
> returns current report list
> ```json
>    [1, "any value from report", {}, true, []]
> ```
> ---

> **global.info[`"report_status"`]**
>
> returns http status code for the report
> ```json
>    200
> ```
> ---

> **global.info[`"report_custom"`]**
>
> returns current report:custom value
> ```json
>    {
>        "yourCustomField": "customValue"
>    }
> ```
>
> ---

> **global.info[`"request_context"`]**
>
> returns current request payload
> ```json
>    {
>        "method": "POST",
>        "headers": {
>            "Content-Length": "109",
>            "Content-Type": "application/json",
>            "Host": "localhost:8000",
>            "User-Agent": "insomnia/2022.4.2",
>            "Accept": "*/*"
>        },
>        "query": {},
>        "body": {
>            "name": "sample_walker",
>            "ctx": {
>                "fieldOne": "1"
>            },
>            "nd": "active:graph",
>            "snt": "active:sentinel"
>        }
>    }
> ```
> ### **Usage:**
> walker can now accept custom payload (non ctx structure). Request body can be access via `globa.info["request_context"]["body"]`
> developers now have control on different request constraints such us method type and headers validation
>
> ---

> **global.info[`"runtime_errors"`]**
>
> returns current runtime error list
> ```json
>[
>   "sentinel1:sample_walker - line 100, col 0 - rule walker - Internal Exception: 'NoneType' object has no attribute 'activity_action_ids'"
>]
> ```
> ---

---
---

# **Report Custom**
Supports custom structure as response body.

## **Syntax**
```js
    report:custom = `{{ any | {} | [] }}`
```

## **Usage**
This can be combine with walker_callback as 3rd party service requires different json structure on response.
It can also be used for different scenario that doesn't require ctx structure
