# **`HOW TO USE ELASTIC`**

## **`SETUP ELASTIC CONFIG`**
```js
ELASTIC_CONFIG = {
    "enabled": true,
    "quiet": false,
    "url": "elastic url",
    "auth": "token for elastic url",
    "common_index": "common-log", // used as fallback when index is not specified
    "activity_index": "activity-log" // used for activity logs
}

ELASTIC_MANIFEST = {/* KUBE MANIFEST */}
```

# **`TYPES ACTIONS`**
## **std** `(Standard)`
- This will be used for standard logging for activity. It uses base structure but can be overriden and add additional fields.


```js
// default structure
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


std.log_activity(
    log: {... fields to be included/overriden in default structure ...},
    action: "your custom name for activity_action",
    query: "additional url query the elastic supports",
    suffix: "optional suffix of index. ex: -{{user's jid}}"
)
```

## **elastic** `(Customizable)`
```js
// most customizable post action
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

// similar to elastic.post but pointed to activity_index
elastic.post_act(url: str, body: dict, suffix: str = "");

// most customizable get action
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

// similar to elastic.get but pointed to activity_index
elastic.get_act(url: str, body: dict, suffix: str = "");

// url is set to `/_doc` but log, query, index and sufix are still customizable
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

// similar to elastic.doc but pointed to activity_index
elastic.doc_activity(log: dict, query: str = "", suffix: str = "");

// url is set to `/_search` but body, query, index and sufix are still customizable
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

// similar to elastic.search but pointed to activity_index
elastic.search_activity(body: dict, query: str = "", suffix: str = "");

// url is set to `/_mapping` but query, index and sufix are still customizable
elastic.mapping(
    query: "additional url query the elastic supports ex: filter_path=aggregations.**.key" // default to empty
    index: "jaseci-elastic-log", // default to common_index
    suffix: "empty or anything here" // default to empty
);

// similar to elastic.mapping but pointed to activity_index
elastic.mapping_activity(query: str = "", suffix: str = "");

// url is set to `/_aliases` but query is still customizable
elastic.aliases(query: str = "pretty=true");

// url is set to `/_reindex` but body, query is still customizable
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