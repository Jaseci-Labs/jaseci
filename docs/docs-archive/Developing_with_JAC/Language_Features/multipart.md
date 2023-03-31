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
