# **`HOW TO USE ELASTIC`**

# **CONFIGURATION**
## **`ATTRIBUTES`**

| Attribute | Description |
| ----------- | ----------- |
| enabled | If service is enabled in config. The service can be available (upon building) but not enabled (from config) |
| quiet | if error logs should be suppressed |
| auth | Api key or token used as Authorization header |
| common_index | default index where elastic log will be saved |
| activity_index | dedicated elastic index for activity logs |
### **`DEFAULT CONFIG`**

```js
ELASTIC_CONFIG = {
    "enabled": false,
    "quiet": false,
    "url": "localhost:9200",
    "auth": null,
    "common_index": "common-log", // used as fallback when index is not specified
    "activity_index": "activity-log" // used for activity logs
}

// default manifest should be enough for now, no changes needed
ELASTIC_MANIFEST = {/* KUBE MANIFEST */}
```

### **`ENABLED CONFIG`**
```js
ELASTIC_CONFIG = {
    "enabled": true,
    "quiet": false,
    "url": "localhost:9200",
    "auth": "ApiKey cVhsYU********************mJPUQ",
    "common_index": "common-log",
    "activity_index": "activity-log"
}

// default manifest should be able to handle automatic spawning of pods for elastic
ELASTIC_MANIFEST = {/* KUBE MANIFEST */}
```
---
# **ACTION LIST**
# **std.`log_activity`**
- This will be used for standard logging for activity.
- It will use base structure and can be overriden or add additional fields.

### **`DEFAULT ACTIVITY LOG STRUCTURE`**
```js
// all of this fields can be overriden
{
    "datetime": date_now,
    "activity_action": "your custom name" or "walker's name using underscore instead of space",
    "activity_type": "walker's name",
    "activity_point": "current node's name",
    "walker_id": "walker's jid",
    "node_id": "current node's jid",
    "master_id": "current user's master jid",
    "user": {
        "email": "current user's email",
        // ---- if accessible ---- //
        "name": "current user's name",
        "id": "current user's id",
        "is_superuser": "current user's details",
        "is_activated": "current user's details",
        // ----------------------- //
    },
    "request_context": {... current http request metadata [global.info["request_context"] ... },
    "data": "current walker's context",
    "misc": {
        "report": "current walker's report list",
        "node": "current node's info"
    }
}
```
##### **`HOW TO TRIGGER`**
```js
std.log_activity(
    log: {... fields to be included/overriden in default structure ...},
    action: "testing_activity", //your custom name for activity_action
    query: "", // additional url query the elastic supports
    suffix: here.jid //"optional suffix of index. ex: -{{user's jid}}"
)
```

# **elastic.`post`**
- This is the post request trigger to elastic.
- url, body, index and suffix can be change
##### **`HOW TO TRIGGER`**
```js
elastic.post(
    url: "your endpoint after elastic url + query",
    body: {
        "your_custom_structure": "any structure",
        "field1": 1,
        "field2": 2
    },
    index: "jaseci-elastic-log", // default to common_index
    suffix: "empty or anything here" // default to empty
);
```
# **elastic.`post_act`**
- similar to elastic.post but always pointed to activity_index
##### **`HOW TO TRIGGER`**
```js
elastic.post_act(url: str, body: dict, suffix: str = "");
```

# **elastic.`get`**
- This is the get request trigger to elastic.
- url, body, index and suffix can be change
##### **`HOW TO TRIGGER`**
```js
elastic.get(
    url: "your endpoint after elastic url + query",
    body: {
        "your_request_body_if_needed": "testing",
        "any_ex_filter": [],
        "any_ex_size": 10
    },
    index: "jaseci-elastic-log", // default to common_index
    suffix: "empty or anything here" // default to empty
);
```
# **elastic.`get_act`**
- similar to elastic.get but always pointed to activity_index
##### **`HOW TO TRIGGER`**
```js
elastic.get_act(url: str, body: dict, suffix: str = "");
```

# **elastic.`doc`**
- this action will used for creation of log
- url will be fixed and always pointed to **`/_doc`** endpoint.
- log, index and suffix can be change
##### **`HOW TO TRIGGER`**
```js
elastic.doc(
    log: {
        "your_custom_structure_if_needed": "any structure",
        "field1": 1,
        "field2": 2
    },
    query: "additional url query the elastic supports ex: filter_path=aggregations.**.key" // default to empty
    index: "jaseci-elastic-log", // default to common_index
    suffix: "empty or anything here" // default to empty
);
```

# **elastic.`doc_activity`**
- similar to elastic.doc but always pointed to activity_index
##### **`HOW TO TRIGGER`**
```js
elastic.doc_activity(log: dict, query: str = "", suffix: str = "");
```

# **elastic.`search`**
- this action will used for retrieval of logs
- url will be fixed and always pointed to **`/_search`** endpoint.
- body, query, index and suffix can be change
##### **`HOW TO TRIGGER`**
```js
elastic.search(
    body: {
        "your_request_body_if_needed": "testing",
        "any_ex_filter": [],
        "any_ex_size": 10
    },
    query: "additional url query the elastic supports ex: filter_path=aggregations.**.key" // default to empty
    index: "jaseci-elastic-log", // default to common_index
    suffix: "empty or anything here" // default to empty
);
```
# **elastic.`search_activity`**
- similar to elastic.search but pointed to activity_index
##### **`HOW TO TRIGGER`**
```js
elastic.search_activity(body: dict, query: str = "", suffix: str = "");
```

# **elastic.`mapping`**
- this action will used for getting mapping of specified index
- url will be fixed and always pointed to **`/_mapping`** endpoint.
- query, index and suffix can be change
##### **`HOW TO TRIGGER`**
```js
elastic.mapping(
    query: "additional url query the elastic supports ex: filter_path=aggregations.**.key" // default to empty
    index: "jaseci-elastic-log", // default to common_index
    suffix: "empty or anything here" // default to empty
);
```

# **elastic.`mapping_activity`**
- similar to elastic.mapping but pointed to activity_index
##### **`HOW TO TRIGGER`**
```js
elastic.mapping_activity(query: str = "", suffix: str = "");
```
# **elastic.`aliases`**
- this action will used for getting aliases
- url will be fixed and always pointed to **`/_aliases`** endpoint.
- query can be change
##### **`HOW TO TRIGGER`**
```js
elastic.aliases(query: str = "pretty=true");
```

# **elastic.`reindex`**
- this action will used for reindexing logs
- url will be fixed and always pointed to **`/_reindex`** endpoint.
- body and query can be change
##### **`HOW TO TRIGGER`**
```js
elastic.reindex(
    body: {
        "source": {
            "index": "act-zsbdev",
                "size": 10
        },
        "dest": {
            "index": "actlog-zsbdev"
        }
    },
    query: "additional url query the elastic supports ex: filter_path=aggregations.**.key" // default to empty
)
```