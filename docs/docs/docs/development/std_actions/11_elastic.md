# Elastic Actions Library

## Enable Elastic in Jaseci

The Elastic service in Jaseci is managed by JSORC, which automatically creates an Elastic container in your kubernetes cluster and connects it with the Jaseci container. If your Jaseci cluster doesn't currently have an Elastic running, you will need to trigger a service refresh on JSORC.

First, make sure Elastic is enabled by setting the `enabled` field in Elastic config to be True. We first get the current config via the `config_get` endpoint. (We are going to use jsctl for the following examples but you can also use API requests)

Run the follwoing command in `jsctl` shell.

```bash
config get ELASTIC_CONFIG
```

This will return a json of the current configuration for the Elastic Service. Check the field and make sure they are configured to your needs. (More details on the configuration attributes below.)

Update the `enabled` field to be True if it is not already.
Then save it with `config_set`.

```bash
config set ELASTIC_CONFIG -value JSON_STRING_OF_THE_CONFIG
```

Final step to enable Elastic is to refresh the Elastic service for the updated configuration to take effect.

```bash
service refresh elastic
```

JSORC will then refresh the Elastic service and creates the neccessary kuberentes resources.

### **CONFIGURATION**

#### **`ATTRIBUTES`**

| Attribute      | Description                                                                                                 |
| -------------- | ----------------------------------------------------------------------------------------------------------- |
| enabled        | If service is enabled in config. The service can be available (upon building) but not enabled (from config) |
| quiet          | if error logs should be suppressed                                                                          |
| auth           | Api key or token used as Authorization header                                                               |
| common_index   | default index where elastic log will be saved                                                               |
| activity_index | dedicated elastic index for activity logs                                                                   |
|                |

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
    "common_index": "kibana-namespace-common",
    "activity_index": "kibana-namespace-activity"
}

// default manifest should be able to handle automatic spawning of pods for elastic
ELASTIC_MANIFEST = {/* KUBE MANIFEST */}
```

## Actions List

### Log Activity

`std.log_activity`

- This will be used for standard logging for activity.
- It will use base structure and can be overriden or add additional fields.
- `misc` inside your created log will use dict's update approach
    -   ```js
        log: {
            "misc": {
                "report": 1,
                "var1": 2
            }
        }

        // created log will look like this
        {
            ...
            "misc": {
                "report": 1, // overriden
                "node": "current node's info",
                "var1": 2 // added
            }
        }
        ```

**`DEFAULT ACTIVITY LOG STRUCTURE`**

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

**`HOW TO TRIGGER`**

```js
std.log_activity(
    log = {... fields to be included/overriden in default structure ...},
    action = "testing_activity", //your custom name for activity_action
    query = "", // additional url query the elastic supports
    suffix = here.jid //"optional suffix of index. ex: -{{user's jid}}"
)
```

### Base Post Request

`elastic._post`

- This is the **`base`** post request trigger to elastic.
- `url`: your complete url after elastic url. you may add query params
- `json`: your request body

**`HOW TO TRIGGER`**

```js
elastic._post(
    url = "/your-index-or-without-index/_doc?pretty=true",
    json = {
        "your_custom_structure": "any structure",
        "field1": 1,
        "field2": 2
    }
);
```

### Post request

`elastic.post`

- This is the post request trigger to elastic.
- `url`: your endpoint after elastic url and index. you may add query params
- `body`: your request body
- `index`: your custom index. defaults to config's common_index
- `suffix`: use to add suffix on current index. usually used in per user index

**`HOW TO TRIGGER`**

```js
elastic.post(
    url = "/_doc?pretty=true",
    body = {
        "your_custom_structure": "any structure",
        "field1": 1,
        "field2": 2
    },
    index = "jaseci-elastic-log", // default to common_index
    suffix = "empty or anything here" // default to empty
);
```

### Post request pointed to `activity_index`

`elastic.post_act`

- similar to elastic.post but always pointed to activity_index.

**`HOW TO TRIGGER`**

```js
elastic.post_act(url: str, body: dict, suffix: str = "");
```

### Base Get request

`elastic._get`

- This is the **`base`** get request trigger to elastic.
- `url`: your complete url after elastic url. you may add query params
- `json`: your request body

**`HOW TO TRIGGER`**

```js
elastic._get(
    url = "/your-index-or-without-index/_search?pretty=true",
    json = {
        "from": 0,
        "size": 10,
        "query": {
            "match_all": {}
        }
    }
);
```

### Get request

`elastic.get`

- This is the get request trigger to elastic.
- `url`: your endpoint after elastic url and index. you may add query params
- `body`: your request body
- `index`: your custom index. defaults to config's common_index
- `suffix`: use to add suffix on current index. usually used in per user index

**`HOW TO TRIGGER`**

```js
elastic.get(
    url = "/_search?pretty=true",
    body = {
        "from": 0,
        "size": 10,
        "query": {
            "match_all": {}
        }
    },
    index = "jaseci-elastic-log", // default to common_index
    suffix = "empty or anything here" // default to empty
);
```

### Get request pointed to `activity_index`

`elastic.get_act`

- similar to elastic.get but always pointed to activity_index

**`HOW TO TRIGGER`**

```js
elastic.get_act(url: str, body: dict, suffix: str = "");
```
### Creation of log

`elastic.doc`

- this action will be used for creation of log
- `url` will always be pointed to **`/_doc`** endpoint.
- `log`: your request log
- `query`: your additional query params
- `index`: your custom index. defaults to config's common_index
- `suffix`: use to add suffix on current index. usually used in per user index

**`HOW TO TRIGGER`**

```js
elastic.doc(
    log = {
        "your_custom_structure_if_needed": "any structure",
        "field1": 1,
        "field2": 2
    },
    query = "additional url query the elastic supports ex: filter_path=aggregations.**.key" // default to empty
    index = "jaseci-elastic-log", // default to common_index
    suffix = "empty or anything here" // default to empty
);
```

### Creation of log with `doc_activity`

`elastic.doc_activity`

- similar to elastic.doc but always pointed to activity_index

**`HOW TO TRIGGER`**

```js
elastic.doc_activity(log: dict, query: str = "", suffix: str = "");
```

### Search

`elastic.search`

- this action will be used for retrieval of logs
- `url` will always be pointed to **`/_search`** endpoint.
- `body`: your request body. Mostly for filtering
- `query`: your additional query params
- `index`: your custom index. defaults to config's common_index
- `suffix`: use to add suffix on current index. usually used in per user index

**`HOW TO TRIGGER`**

```js
elastic.search(
    body = {
        "from": 0,
        "size": 10,
        "query": {
            "match_all": {}
        }
    },
    query = "additional url query the elastic supports ex: filter_path=aggregations.**.key" // default to empty
    index = "jaseci-elastic-log", // default to common_index
    suffix = "empty or anything here" // default to empty
);
```

### Search with search activity

`elastic.search_activity`

- similar to elastic.search but always pointed to activity_index

**`HOW TO TRIGGER`**

```js
elastic.search_activity(body: dict, query: str = "", suffix: str = "");
```

### Mapping

`elastic.mapping`

- this action will be used for getting mapping of specified index
- `url` will always be pointed to **`/_mapping`** endpoint.
- `query`: your additional query params
- `index`: your custom index. defaults to config's common_index
- `suffix`: use to add suffix on current index. usually used in per user index

**`HOW TO TRIGGER`**

```js
elastic.mapping(
    query = "additional url query the elastic supports ex: filter_path=aggregations.**.key" // default to empty
    index = "jaseci-elastic-log", // default to common_index
    suffix = "empty or anything here" // default to empty
);
```

### Mapping with `mapping_activity`

`elastic.mapping_activity`

- similar to elastic.mapping but always pointed to activity_index

**`HOW TO TRIGGER`**

```js
elastic.mapping_activity(query: str = "", suffix: str = "");
```

### Refresh

`elastic.refresh`

- this action will be used for manual refresh
- `url` will always be pointed to **`/_refresh`** endpoint.
- `index`: your custom index. defaults to config's common_index
- `suffix`: use to add suffix on current index. usually used in per user index

**`HOW TO TRIGGER`**

```js
elastic.refresh(
    index = "jaseci-elastic-log", // default to common_index
    suffix = "empty or anything here" // default to empty
);
```

### Refresh wirh `refresh_activity`

`elastic.refresh_activity`

- similar to elastic.refresh but always pointed to activity_index

**`HOW TO TRIGGER`**

```js
elastic.refresh_activity(suffix: str = "");
```

### Aliases

`elastic.aliases`

- this action will used for getting aliases
- `url` will always be pointed to **`/_aliases`** endpoint.
- `query`: your additional query params

**`HOW TO TRIGGER`**

```js
elastic.aliases(query = "pretty=true");
```

### Reindex

`elastic.reindex`
- this action will used for reindexing logs
- `url` will always be pointed to **`/_reindex`** endpoint.
- `body`: your request body
- `query`: your additional query params

**`HOW TO TRIGGER`**

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
```s