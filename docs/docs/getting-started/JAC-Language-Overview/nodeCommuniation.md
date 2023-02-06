---
title: Walker to Node communication
---

The `here` keyword is used reference the node the walker is currently on.

```jac
walker talker {
    has utterance;

    state {
        #the message and prompts attribute of the current node will be printed
        std.out(here.message, here.prompts);

        utterance = std.input("> ");

        if(utterance == "quit"): disengage;

        take -[transition(intent == utterance)]-> node::state else {
            take here;
        }
    }
}

```
The `visitor` keyword is used to reference attributes of the walker from the node it is currently on.

```jac
node state{
    has prev_value;

    can getvalue with talker entry {
        here.prev_value = visitor.value;
        std.out(here.prev_value);
    }
}
```