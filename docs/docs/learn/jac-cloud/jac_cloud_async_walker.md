# Jac Cloud Async Walker

```python
async walker sample {
    has value: int = 0;

    can enter with `root entry {
        print("test");
        self.value = 1;
    }
}
```

- Async walker will be triggered as task similar to [create_task](./jac_cloud_scheduler.md#jac-cloud-optional-task)
- It will be run concurrently on different thread

## `Response`

```json
{ "walker_id": "w:sample:{uuid}" }
```

## `Get Result`

```python
walker view_sample_result {
    has walker_id: str;

    can enter with `root entry {
        wlk = &walker_id;
        print(wlk.value); # will be 1

        # `wlk.__jac__.schedule` have everything related to database status
        # status, node_id, root_id, execute_date, executed_date, http_status, reports, custom, error
    }

}
```
