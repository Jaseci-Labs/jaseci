---
title : Functions
---

Nodes and Walkers can have unique abilities. These are  much like functions. They can be executed in different scenarios.

## Nodes and Functions

The basic syntax for a function is as follows. Walkers can execute this code by simply using `here.[name of function] `

```jac
node [name of node ] {
    can [name of function] {

        # enter code to be executed here
    }
}
```

### Execute with entry and exit

Node functions can be executed when a walker traverses on to it or when a walker leaves
```jac
node [name of node ]  {
    can [name of function]entry  {

        # enter code to be executed when walker traverses on this node
    }

      can [name of function] exit {

        # enter code to be executed when walker leaves this node
    }
}

```

### Execute with sepcific walker

Nodes can have their functions only executed by a specific walker

```jac
node [name of node ] {
    can [name of function] with [namme of walker ] {

        # enter code to be executed here
    }
}
```

### Excute with specific walker on entry and exit

```jac
node [name of node ] {
    can [name of function] with [namme of walker ] entry {

        # enter code to be executed here
    }
      can [name of function] with [namme of walker ] exit{

        # enter code to be executed here
    }
}
```

### Examlpes

#### Actions and Abilities in Walkers

```jac
node person {
    has name;
    has byear;
    can set_year with setter entry {
        byear = visitor.year;
    }
    can print_out with exit {
        std.out(byear," from ",visitor.info);
    }
    can reset { #<-- Could add 'with activity' for equivalent behavior
        ::set_back_to_95;
        std.out("resetting year to 1995:", here.context);
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

### Functions(Abilities) in Nodes

```jac
node person {
    has name;
    has byear;
    can set_year with setter entry {
        byear = visitor.year;
    }
    can print_out with exit {
        std.out(byear," from ",visitor.info);
    }
    can reset { //<-- Could add 'with activity' for equivalent behavior
        byear="1995-01-01";
        std.out("resetting birth year to 1995:", here.context);
    }
}

walker init {
    has year=std.time_now();
    root {
        person1 = spawn here --> node::person;
        std.out(person1);
        person1::reset;
        take --> ;
    }
    person {
        spawn here walker::setter;
        here::reset(name="Joe");
    }
}

walker setter {
    has year=std.time_now();
}
```