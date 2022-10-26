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