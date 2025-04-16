# Indexing
* jac-cloud support indexing. However, it's limited to mongodb partialFilterExpression as we use a single collection for each architypes [`node`, `edge`, `object`, `walker`]
- while index without contraints is still supported, it might not be as useful as we usually querying architype by `_id`. It will only be useful if we manually querying it.
- **`by rule`**, this will always apply with partialFilterExpression constraints for name
```python
{
  "partialFilterExpression": {
    "name": {{the_name_of_the_architype}}
  }
}
```
# How To Use
### `SINGLE INDEX`
```python
node UniqueNode {
    has id: str;

    static has  __jac_indexes__: list = [{
        "key": {"id": 1} # 1 ASC, -1 DESC
    }];
}
```

### `COMPOUND INDEX`
```python
node UniqueNode {
    has id1: str;
    has id2: str;

    static has  __jac_indexes__: list = [{
        "key": {"id1": 1, "id2": 1} # 1 ASC, -1 DESC
    }];
}
```

### `UNIQUE CONSTRAINTS`
```python
node UniqueNode {
    has id: str;

    static has  __jac_indexes__: list = [{
        "key": {"id": 1}, # 1 ASC, -1 DESC
        "constraints": {"unique": True}
    }];
}
```

## For additional constraints options, you may check mongodb [docs](https://www.mongodb.com/docs/manual/indexes/) for indexing for more info.