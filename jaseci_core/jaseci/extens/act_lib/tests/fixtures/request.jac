walker sample {
    can request.trigger;

    with entry {
        report request.trigger("get", "https://dummyjson.com/products/1");
        report request.trigger("post", "https://dummyjson.com/products/add", json={
            "title": "Testing"
        });
        report request.trigger("put", "https://dummyjson.com/products/1", json={
            "title": "Testing2"
        });
    }
}