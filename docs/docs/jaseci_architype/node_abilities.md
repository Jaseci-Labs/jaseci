# Node Abilities

```jac
node person {
    has name;
    has byear;
    can set_year with setter entry {
        byear = visitor.year;
    }
    can print_out with exit {
        std.out(byear,"␣from␣",visitor.info);
    }
    can reset { #<-- Could add 'with activity' for equivalent behavior
        ::set_back_to_95;
        std.out("resetting␣year␣to␣1995:", here.context);
    }
    can set_back_to_95: byear="1995-01-01";
 }

 walker init {
    has year=std.time_now();
    can setup {
        person1 = spawn here --> node::person;
        std.out(person1);
        person1::reset;
    }
    root {
        ::setup;
        take --> ;
    }
    person {
        spawn here walker::setter;
        person1::reset(name="Joe");
    }
 }

 walker setter {
    has year=std.time_now();
 }
```

The code provided offers an illustration of how to define a node equipped with abilities in Jaseci language. In this example, the "person" node comes with two attributes, "name" and "byear". The "set_year" ability executes on entry and updates the "byear" attribute based on the value of the "visitor.year" parameter. Similarly, the "print_out" ability executes on exit and outputs the "byear" attribute alongside the "visitor.info".

Moreover, the "reset" ability does not execute on entry or exit but sets the "byear" attribute to "1995-01-01". The "walker init" is equipped with a "setup" ability, which creates a "person" node and invokes the "reset" ability. The walker then advances to the next node and repeats the same steps.

Another walker, named "setter", comes with a "year" attribute and gets activated when a "person" node is created. This walker can be utilized to trigger the "set_year" ability. It's worth noting that abilities are self-contained in-memory compute operations, which can interact with the context and local variables of the node/edge/walker to which they are attached, without returning any value.

