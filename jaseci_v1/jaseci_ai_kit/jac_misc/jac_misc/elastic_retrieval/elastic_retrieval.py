from openai import OpenAI
from os import environ, unlink
from datetime import datetime
from requests import get
from uuid import uuid4

from .utils import extract_text_from_file, get_embeddings, generate_chunks, extraction
from jaseci.jsorc.live_actions import jaseci_action
from elasticsearch import Elasticsearch

OAI_CLIENT = None
ES_CLIENT = None
CONFIG = {
    "elastic": {
        "url": environ.get("ELASTICSEARCH_URL", "http://localhost:9200"),
        "key": environ.get("ELASTICSEARCH_API_KEY"),
        "index_template": {
            "name": environ.get("ELASTICSEARCH_INDEX_TEMPLATE") or "openai-embeddings",
            "index_patterns": (
                environ.get("ELASTICSEARCH_INDEX_PATTERNS") or "oai-emb-*"
            ).split(","),
            "priority": 500,
            "version": 1,
            "template": {
                "settings": {
                    "number_of_shards": int(environ.get("ELASTICSEARCH_SHARDS", "1")),
                    "number_of_replicas": int(
                        environ.get("ELASTICSEARCH_REPLICAS", "1")
                    ),
                    "refresh_interval": "1s",
                },
                "mappings": {
                    "_source": {"enabled": True},
                    "properties": {
                        "id": {"type": "keyword"},
                        "embedding": {
                            "type": "dense_vector",
                            "dims": int(
                                environ.get("ELASTICSEARCH_VECTOR_SIZE", "1536")
                            ),
                            "index": True,
                            "similarity": environ.get(
                                "ELASTICSEARCH_SIMILARITY", "cosine"
                            ),
                        },
                        "version": {"type": "keyword"},
                    },
                },
            },
        },
    },
    "openai": {"api_key": environ.get("OPENAI_API_KEY")},
    "openai_embedding": {
        "model": environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-ada-002"),
    },
    "chunk_config": {
        "chunk_size": int(environ.get("CHUNK_SIZE", "200")),
        "min_chunk_size_chars": int(environ.get("MIN_CHUNK_SIZE_CHARS", "350")),
        "min_chunk_length_to_embed": int(environ.get("MIN_CHUNK_LENGTH_TO_EMBED", "5")),
        "max_num_chunks": int(environ.get("MAX_NUM_CHUNKS", "10000")),
    },
    "batch_size": int(environ.get("BATCH_SIZE", "100")),
}


@jaseci_action(act_group=["es_ret"], allow_remote=True)
def setup(config: dict = CONFIG, rebuild: bool = False, reindex_template: bool = False):
    global CONFIG, ES_CLIENT, OAI_CLIENT
    CONFIG = config

    if rebuild:
        ES_CLIENT = None
        OAI_CLIENT = None

    if reindex_template:
        reapply_index_template()


@jaseci_action(act_group=["es_ret"], allow_remote=True)
def upsert(index: str, data: dict, reset: bool = False, refresh=None, meta: dict = {}):
    bs = CONFIG["batch_size"]

    doc_u = data.get("url", [])
    doc_t = data.get("text", [])

    # only works if not remote
    doc_f = data.get("file", [])

    if reset:
        reset_index(index)
    else:
        delete(
            index,
            [doc["id"] for doc in doc_t]
            + [doc["id"] for doc in doc_u]
            + [doc["id"] for doc in doc_f],
        )

    doc_a = []
    for doc in doc_u:
        file_name: str = "/tmp/" + (doc.pop("name", None) or str(uuid4()))
        with get(doc.pop("url"), stream=True) as res, open(file_name, "wb") as buffer:
            res.raise_for_status()
            for chunk in res.iter_content(chunk_size=8192):
                buffer.write(chunk)

        doc["text"] = extract_text_from_file(file_name)

        unlink(file_name)
        doc_a += generate_chunks(doc, CONFIG["chunk_config"])

    for doc in doc_t:
        doc_a += generate_chunks(doc, CONFIG["chunk_config"])

    hook = meta.get("h")
    if hasattr(hook, "get_file_handler"):
        for doc in doc_f:
            fh = hook.get_file_handler(doc["file"])
            doc["text"] = extract_text_from_file(fh.absolute_path)
            doc_a += generate_chunks(doc, CONFIG["chunk_config"])

    ops_index = {"index": {"_index": index}}
    ops_t = []
    for docs in [doc_a[x : x + bs] for x in range(0, len(doc_a), bs)]:
        for i, emb in enumerate(
            get_embeddings([doc["text"] for doc in docs], *openai())
        ):
            docs[i]["embedding"] = emb
            docs[i]["created_time"] = int(
                datetime.fromisoformat(docs[i]["created_time"]).timestamp()
            )
            ops_t.append(ops_index)
            ops_t.append(docs[i])

    elastic().bulk(operations=ops_t, index=index, refresh=refresh)

    return True


@jaseci_action(act_group=["es_ret"], allow_remote=True)
def delete(index: str, ids: list = [], all: bool = False):
    if all:
        return reset_index(index)
    elif ids:
        return (
            elastic()
            .delete_by_query(
                index=index,
                query={"terms": {"id": ids}},
                ignore_unavailable=True,
            )
            .body
        )


@jaseci_action(act_group=["es_ret"], allow_remote=True)
def query(index: str, data: list):
    bs = CONFIG["batch_size"]

    search_index = {"index": index}
    searches = []
    for queries in [data[x : x + bs] for x in range(0, len(data), bs)]:
        for i, emb in enumerate(
            get_embeddings(
                [query["query"] for query in queries],
                *openai(),
            )
        ):
            top = queries[i].get("top") or 3
            query = {
                "knn": {
                    "field": "embedding",
                    "query_vector": emb,
                    "k": top,
                    "num_candidates": queries[i].get("num_candidates") or (top * 10),
                    "filter": queries[i].get("filter") or [],
                }
            }

            min_score = queries[i].get("min_score")
            if min_score:
                query["min_score"] = min_score

            searches.append(search_index)
            searches.append(query)

    return [
        {
            "query": query,
            "results": [
                {
                    "id": hit["_source"]["id"],
                    "text": hit["_source"]["text"],
                    "score": hit["_score"],
                }
                for hit in result["hits"]["hits"]
            ],
        }
        for query, result in zip(
            queries,
            elastic().msearch(searches=searches, ignore_unavailable=True)["responses"],
        )
    ]


@jaseci_action(act_group=["es_ret"], allow_remote=True)
def reset_index(index: str):
    return elastic().indices.delete(index=index, ignore_unavailable=True).body


@jaseci_action(act_group=["es_ret"], allow_remote=True)
def reapply_index_template():
    return (
        elastic().indices.put_index_template(**CONFIG["elastic"]["index_template"]).body
    )


@jaseci_action(act_group=["es_ret"], allow_remote=True)
def file_is_readable(id: str, meta: dict = {}):
    """temp"""
    from jaseci.utils.file_handler import FileHandler

    file_handler: FileHandler = meta["h"].get_file_handler(id)
    try:
        with file_handler.open(mode="rb", detached=True) as buff:
            if extraction(buff):
                return True
    except Exception:
        pass

    return False


def openai() -> OpenAI:
    global CONFIG, OAI_CLIENT
    if not OAI_CLIENT:
        try:
            OAI_CLIENT = OpenAI(**CONFIG["openai"])
        except Exception as e:
            raise e
    return OAI_CLIENT, CONFIG["openai_embedding"]


def elastic() -> Elasticsearch:
    global CONFIG, ES_CLIENT
    if not ES_CLIENT:
        config = CONFIG.get("elastic")
        try:
            client = Elasticsearch(
                hosts=[config["url"]],
                api_key=config["key"],
                request_timeout=config.get("request_timeout"),
            )
            client.info()
            ES_CLIENT = client
        except Exception as e:
            raise e
    return ES_CLIENT
