[<< back to main](../README.md)
# **jac-cloud**

## **How To Start**
- `FastAPI.start` will convert walkers to FastAPI endpoints
- as default, `jac_cloud` have base user and sso apis

## **Supported Args**
| **NAME**  | **DESCRIPTION**   | **ENVIRONMENT VARIABLE**  | **DEFAULT**   |
|-----------|-------------------|---------------------------|---------------|
| **host**      | your local host   | HOST                      | 0.0.0.0       |
| **port**      | your local port   | PORT                      | 8000          |
| **emailer**   | overrided `jac_cloud.jaseci.utils.Emailer` | N/A | N/A      |
| {**kwargs} | any fields that's currently supported in `uvicorn.run` | N/A | N/A |

```python
import:py from jac_cloud {FastAPI}

with entry:__main__ {
    FastAPI.start(
        host="0.0.0.0",
        port=8001
    );
}
```
## **OPENAPI** (`/docs`)
![Default APIs](https://private-user-images.githubusercontent.com/74129725/355489885-ea5406a0-7a49-4fd2-b77d-10555e5100fb.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MjI5NTQ5ODksIm5iZiI6MTcyMjk1NDY4OSwicGF0aCI6Ii83NDEyOTcyNS8zNTU0ODk4ODUtZWE1NDA2YTAtN2E0OS00ZmQyLWI3N2QtMTA1NTVlNTEwMGZiLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDA4MDYlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQwODA2VDE0MzEyOVomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTk1MjNiM2EzYjI1MzM1Njk5MzdjNDRkYjExMzdiMzQ3MjczNzY1ODdkYTVhNmNlNGRiMjNmOWI2ZGQxMDY4ODgmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JmFjdG9yX2lkPTAma2V5X2lkPTAmcmVwb19pZD0wIn0.nW6DNC3BBf98J0VGdpstXtsRdVrLIc85EJOo_00YyTs "Default APIs")


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

with entry:__main__ {
    FastAPI.start(
        host="0.0.0.0",
        port=8001
    );
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