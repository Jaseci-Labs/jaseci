# Jac Cloud

## **How To Start**
Just replace `jac run` with `jac serve` and you are now running your jac application as an API server.


`jac serve main.jac`

Optionally, specif host and port with `--host` and `--port`.

Once starts, navigate to `/docs` to access the built-in API docs.


## **Walker Endpoints**
- as default, walker declaration will be converted to 2 group of endpoints but can be disable by setting environment variable `DISABLE_AUTO_ENDPOINT=true`
    - group will be based on allowed `methods` and `path` on specs
    - group 1: `/walker/{walker's name}`
    - group 2: `/walker/{walker's name}/{node}`
- to control enpoint specification, you need to declare inner `class __specs__ {}` or `obj __specs__ {}`. You may also use `@specs` from `jac_cloud.plugin.jaseci.specs` if you have disabled auto endpoint
- walker support all kind of http method and all fastapi's supported object as path variable / query parameters / json body / file

## **Supported specs**
| **NAME**  | **TYPE**  | **DESCRIPTION**   | **DEFAULT**   |
|-----------|-----------|-------------------|---------------|
| path      | str       | additional path after default auto generated path **[root]:**`walker/{walker's name}`**/{your path}** or **[node]:**`walker/{walker's name}/{node id}`**/{your path}** | N/A |
| methods   | list[str] | list of allowed http methods lowercase | ["post"] |
| as_query  | str \| list[str] | list of declared fields that's intended to be query params. Setting it to `"*"` will set all fields to be query params | [] |
| auth      | bool      | if endpoint requires authentication or not | true
| private   | bool      | only applicable if auto endpoint is enabled. This will skip the walker in auto generation. | false

## **Examples**
```python
import:py from jac_cloud {FastAPI}

walker post_no_body {}

walker post_with_body {
    has a: str;
}

walker get_no_body {
    obj __specs__ {
        static has methods: list = ["get"];
    }
}

walker get_with_query {
    has a: str;

    obj __specs__ {
        static has methods: list = ["get"], as_query: list = ["a"];
    }
}

walker get_all_query {
    has a: str;
    has b: str;

    obj __specs__ {
        static has methods: list = ["get"], as_query: list = "*", auth: bool = False;
    }
}

walker post_path_var {
    has a: str;

    obj __specs__ {
        static has path: str = "/{a}", methods: list = ["post", "get"];
    }
}

walker combination1 {
    has a: str;
    has b: str;
    has c: str;

    obj __specs__ {
        static has methods: list = ["post", "get"], as_query: list = ["a", "b"];
    }
}


walker combination2 {
    has a: str;
    has b: str;
    has c: str;

    obj __specs__ {
        static has path: str = "/{a}", methods: list = ["post", "get", "put", "patch", "delete", "head", "trace", "options"], as_query: list = ["b"];
    }
}

walker post_with_file {
    has single: UploadFile;
    has multiple: list[UploadFile];
    has singleOptional: UploadFile | None = None;


    can enter with `root entry {
        print(self.single);
        print(self.multiple);
        print(self.singleOptional);
    }

    obj __specs__ {}
}

walker post_with_body_and_file {
    has val: int;
    has single: UploadFile;
    has multiple: list[UploadFile];
    has optional_val: int = 0;

    can enter with `root entry {
        print(self.val);
        print(self.optional_val);
        print(self.single);
        print(self.multiple);
    }

    obj __specs__ {
        static has auth: bool = False;
    }
}
```

## **Walker Response Structure**
- Response support auto serialization of walker/edge/node architypes and obj as long as it's attributes is also serializable (ex: nested dataclass)

```python
{
    "status": {{ int : http status code }},
    "reports": {{ list : jac reports }},

    # optional via SHOW_ENDPOINT_RETURNS=true environment variable
    "returns" {{ list : jac per visit return }}
}
```

## **Walker/Edge/Node Serialization**
```python
{
    "id": {{ str : anchor ref_id }},
    "context": {{ dict : anchor architype data }}
}
```