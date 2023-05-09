---
sidebar_position: 9
---

# Yield

We have so far examined walkers that carry variables and state as they move around a graph. Each time a walk is completed, a walker's state is cleared by default , but node/edge state is preserved. Nevertheless, there are circumstances in which you would want a walker to maintain its state across runs, or even to pause in the middle of a walk and wait to be explicitly called again, updating a subset of its dynamic state. This is where the `yield` keyword comes in.

To see an example of `yield` in action in below.

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
        spawn -->[0] walker::build_example;
        take -->;
    }
person {
        report here.context;
        take -->;
        yield;
    }
}
```

Expected Output:
```json
{
  "success": true,
  "report": [
    {
      "name": "Joe"
    }
  ],
  "final_node": "urn:uuid:b7ebf434-bd90-443a-b8e2-c29589c3da57",
  "yielded": true
}
```

The yield keyword in example 9 instructs the walker simple_yield to stop walking and wait to be called again, even though the walker is instructed to `take-->` edges. In this example, a single next node location is queued up and the walker reports a single here.context each time it’s called, taking only 1 edge per call.

Also note yield can be followed by a number of operations as a shorthand. For example `take-->;` and `yield;` could be combined to a single line with `yield take -->;`. We call
this a `yield-take`. Shorthands include,
- Yield-Take: `yield take -->;`
- Yield-Report: yield `report "hi";`
- Yield-Disengage: `yield disengage; and yield disengage report "bye";`

In each of these cases, the `take`, `report`, and `disengage` executes with the `yield`.

**Technical Semantics of Yield**

There are several key semantics of `yield` to remember, including:

1. Upon a yield, a report is returned back and cleared.
2. Additional report items from further walking will be return on subsequent yields or walk completion.
3. Like the take command, the entire body of the walker will execute on the current node and actually yield at the end of this execution.
• Note: Keep in mind yield can be combined with disengage and skip commands.
1. If a start node, also known as a "prime" node, is supplied while continuing a walker after a yield, the walker will disregard this prime node and continue from where it left off on its journey if there are still other walk nodes it is planned to visit.
2. If there are no nodes scheduled for the walker to go to next, a prime node must be specified (or the walker will continue from root by default).
3. with `entry` and with `exit` code blocks in the walker are not executed upon continuing from a `yield` or executing a `yeild` respectively. Regardless of how many yields there are in between, they only execute once at the beginning and finish of a walk.
4. At the level of the master (user) abstraction, Jaseci maintains the distinction between walkers that have been yielded and need to be resumed and those that are currently being run. The semantics of walkers that are summoned as public are currently unclear. For customized yield behaviors, developers should use the more basic walker spawn and walker execute APIs.
