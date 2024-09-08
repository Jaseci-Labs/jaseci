# **Elastic Retrieval (`elastic_retrieval`)**
- Original source - [ChatGPT Retrieval Plugin](https://github.com/openai/chatgpt-retrieval-plugin)
- This retrieval plugin is for elasticsearch datasource only

## **CONFIGURATION**
### `BATCH HANDLER`
> export **BATCH_SIZE**=`{% batch size handler per request %}` *(default: 100)*
### `ELASTICSEARCH PARAMS`
> export **ELASTICSEARCH_URL**=`{% url of your elasticsearch %}` *(required)*\
> export **ELASTICSEARCH_API_KEY**=`{% api_key of you elasticsearch %}` *(required)*\
> export **ELASTICSEARCH_INDEX_TEMPLATE**=`{% index_template name %}` *(default: openai-embeddings)*\
> export **ELASTICSEARCH_INDEX_PATTERNS**=`{% index_template pattern %}` *(default: oai-emb-\*)*\
> export **ELASTICSEARCH_REPLICAS**=`{% replica count for your index %}` *(default: 1)*\
> export **ELASTICSEARCH_SHARDS**=`{% shard count for your index %}` *(default: 1)*\
> export **ELASTICSEARCH_VECTOR_SIZE**=`{% dense_vector dims value %}` *(default: 1536)*\
> export **ELASTICSEARCH_SIMILARITY**=`{% similarity type %}` *(default: cosine)*
### `OPENAI API KEY`
> export **OPENAI_API_KEY**=`{% openai api_key %}` *(required)*
### `OPENAI OPTIONAL PARAMETERS`
> export **OPENAI_API_BASE**=`{% ex: https://<AzureOpenAIName>.openai.azure.com/ %}`\
> export **OPENAI_API_TYPE**=`{% ex: azure %}`\
> export **OPENAI_EMBEDDING_MODEL**=`{% ex: text-embedding-ada-002 %}`\
> export **OPENAI_EMBEDDING_DEPLOYMENT_ID**=`{% deployment_model %}`\
### `CHUNKING PARAMETERS`
> export **CHUNK_SIZE**=`{% chunking_size %}` *(default: 200)*\
> export **MIN_CHUNK_SIZE_CHARS**=`{% minimum_chunking_size by chars count %}` *(default: 350)*\
> export **MIN_CHUNK_LENGTH_TO_EMBED**=`{% minimum_chunking_length to ignore on embeddings %}` *(default: 5)*\
> export **MAX_NUM_CHUNKS**=`{% maximum_chunks_count %}` *(default: 10000)*
---
# **HOW TO USE**
## es_ret.**`setup`**
> **`Arguments`:** \
> **config**: dict \
> **rebuild**: bool = False \
> **reindex_template**: bool = False
>
> **`Return`:** \
> None
>
> **`Usage`:** \
> to configure elastic retrieval \
> **rebuild**: will rebuild elastic client based on latest config \
> **reindex_template**: will reupdate index template using latest config
>
##### **`HOW TO TRIGGER`**
```js
es_ret.setup({
    "elastic": {
        "url": "https://elastic-----url.com",
        "key": "----------------------------------",
        "index_template": {
            "name": "openai-embeddings",
            "index_patterns": ["oai-emb-*"],
            "priority": 500,
            "version": 1,
            "template": {
                "settings": {
                    "number_of_shards": 1,
                    "number_of_replicas": 1,
                    "refresh_interval": "1s"
                },
                "mappings": {
                    "_source": {"enabled": true},
                    "properties": {
                        "embedding": {
                            "type": "dense_vector",
                            "dims": 1536,
                            "index": true,
                            "similarity": "cosine"
                        },
                        "id": {"type": "keyword"},
                        "version": {"type": "keyword"}
                    }
                }
            }
        }
    },
    "openai": {
        "key": "----------------------------------",
        "embedding": {
            "model": "text-embedding-ada-002"
        }
    },
    "chunk_config": {
        "chunk_size": 200,
        "min_chunk_size_chars": 350,
        "min_chunk_length_to_embed": 5,
        "max_num_chunks": 10000
    },
    "batch_size": 100
}, false, false);
```
---
## es_ret.**`upsert`**
> **`Arguments`:** \
> **index**: str \
> **data**: dict \
> **reset**: bool = False \
> **refresh**: bool = None
>
> **`Return`:** \
> **bool**: true for success else false
>
> **`Usage`:** \
> to insert entry \
> **reset**: will clean the target index \
> **refresh**: [refresh option](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-refresh.html) - ex: `wait_for`
>
##### **`HOW TO TRIGGER`**
```js
es_ret.upsert(
    "oai-emb-your-index-base-on-template",
    {
        "text": [
            {
                "id": "preferably uuid",
                "text": "your text",
                "version": "any string can used as filter on query",
                "created_time": "int timestamp"
            },
            ...
        ],
        "url": [
            {
                "id": "preferably uuid",
                "url": "file url",
                "name": "file name",
                "version": "any string can used as filter on query",
                "created_time": "int timestamp"
            },
            ...
        ],
        "file": [
            {
                "id": "preferably uuid",
                "file": "file_handler uuid", // only works with local module
                "name": "file name",
                "version": "any string can used as filter on query",
                "created_time": "int timestamp"
            },
            ...
        ]
    },
    true,
    "wait_for"
);
```
---
## es_ret.**`delete`**
> **`Arguments`:** \
> **index**: str \
> **ids**: list \
> **all**: bool = False
>
> **`Return`:** \
> **dict**: based on elasticsearch response for index deletion or delete by query
>
> **`Usage`:** \
> to delete by id or the whole index \
> **ids**: your id list \
> **all**: ignore the id list and just delete the index
>
##### **`HOW TO TRIGGER`**
```js
es_ret.delete(all = true);
```
---
## es_ret.**`query`**
> **`Arguments`:** \
> **index**: str \
> **data**: dict \
>
> **`Return`:** \
> **dict**: based on elasticsearch response for msearch
>
> **`Usage`:** \
> top is equivalent to `k` params for knn query\
> you may refer to this [docs](https://www.elastic.co/guide/en/elasticsearch/reference/current/knn-search.html) for additional information
>
##### **`HOW TO TRIGGER`**
```js
es_ret.query(
    "oai-emb-your-index-base-on-template",
    [
        {
            "query": "question-1?",
            "filter": [{
                "term": {"version": "draft"}
            }],
            "top": 3,
            "num_candidates": 100
        }
    ]
);
```
##### **`RESPONSE`**
```js
{
    "query": {
        "query": "question-1?",
        "filter": [{
            "term": {"version": "draft"}
        }],
        "top": 3,
        "num_candidates": 100
    },
    "results": [
        {
            "id": "id-1",
            "text": "answer-1",
            "score": 0.9398868
        },
        {
            "id": "id-2",
            "text": "answer-2",
            "score": 0.9317168
        },
        {
            "id": "id-3",
            "text": "answer-3",
            "score": 0.9314629
        }
    ]
}
```
---
## es_ret.**`reset_index`**
> **`Arguments`:** \
> **index**: str
>
> **`Return`:** \
> **dict**: based on elasticsearch response for index deletion
>
> **`Usage`:** \
> to delete index
>
##### **`HOW TO TRIGGER`**
```js
es_ret.reset_index("oai-emb-your-index-base-on-template");
```
---
## es_ret.**`reapply_index_template`**
> **`Return`:** \
> **dict**: based on elasticsearch response for index put_index_template
>
> **`Usage`:** \
> to update index template based on latest configuration
>
##### **`HOW TO TRIGGER`**
```js
es_ret.reapply_index_template();
```