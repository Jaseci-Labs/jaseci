---
sidebar_position: 6
---

# Ignore

The quite handy command `ignore` from Jaseci allows you to skip(ignore) visiting nodes or edges when traversing.


```jac
node person: has name;
edge family;
edge friend;

walker build_example {
    spawn here +[friend]+> node::person(name="Joe");
    spawn here +[friend]+> node::person(name="Susan");
    spawn here +[family]+> node::person(name="Matt");
    spawn here +[family]+> node::person(name="Dan");
    }

walker init {
    root {
        spawn here walker::build_example;
    ignore -[family]->;
    take -->;
    }
person {
    std.out(here.name);
    take-->;
    }
}
```

Expected Output:

```json
Joe
Susan
```