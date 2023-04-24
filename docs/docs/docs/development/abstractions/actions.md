---
sidebar_position: 4
---

# Actions

Actions share the semantics as traditional function calls with returns, however these primarily serve to enable bindings to the functionality described outside of Jac/Jaseci (ie in a python module). These are comparable to library calls in conventional programming languages. Actions are essentially bindings to external functionality takes the form of a Jaseci action library’s direct connection to Python implementations.

> **Note**
>
> This action interface is the abstraction that allows Jaseci to do it's sophisticated serverless inter-machine optimizations, auto-scaling, auto-componentization etc.

### Jaseci Standard Actions

Jaseci has set of inbuilt actions. Also you can load and unload actions in `jsctl` shell. to see the available actions in jaseci session try running `actions list`. Here is a basic example of jaseci `date` actions.

**Example:**

```jac
node person {
    has name;
    has birthday;
}

walker init {
    can date.quantize_to_year;
    can date.quantize_to_month;
    can date.quantize_to_week;

    person1 = spawn here ++> node::person(name="Josh", birthday="1995-05-20");

    birthyear = date.quantize_to_year(person1.birthday);
    birthmonth = date.quantize_to_month(person1.birthday);
    birthweek = date.quantize_to_week(person1.birthday);

    std.out("Date ", person1.birthday);
    std.out("Quantized date to year ", birthyear);
    std.out("Quantized date to month ", birthmonth);
    std.out("Quantized date to week ", birthweek);
}
```
**Output:**
```
Date  1995-05-20
Quantized date to year  1995-01-01T00:00:00
Quantized date to month  1995-05-01T00:00:00
Quantized date to week  1995-05-15T00:00:00
```