---
sidebar_position: 4
description: An Overview of Actions and Examples.
---

# Actions

Actions share the semantics as traditional function calls with returns, however these primarily serve to enable bindings to the functionality described outside of Jac/Jaseci (ie in a python module). These are comparable to library calls in conventional programming languages. Actions are essentially bindings to external functionality takes the form of a Jaseci action library’s direct connection to Python implementations.

> **Note**
>
> This action interface is the abstraction that allows Jaseci to do it's sophisticated serverless inter-machine optimizations, auto-scaling, auto-componentization etc.
>

### Jaseci Standard Actions

Jaseci has set of inbuilt actions. Also you can load and unload actions in `jsctl` shell. to see the available actions in jaseci session try running `actions list`. Here is a basic example of jaseci `date` actions.


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

Expected output:

```
Date  1995-05-20
Quantized date to year  1995-01-01T00:00:00
Quantized date to month  1995-05-01T00:00:00
Quantized date to week  1995-05-15T00:00:00
```

### Actions Call

Action call allows the user to call a loaded action from the JSCTL. This is useful when you need to test out a action without writing a JAC file. You can just pass the context(parameters) with the command and the action will be called.

```bash
jaseci > actions call <action_name> -ctx <context>
```

example using the standard actions rand.integer to get a random integer between 0 and 10 (you can list the actions using the `actions list` command)

```bash
jaseci > actions call rand.integer -ctx '{"start":0, "end":10}'
```

You can perform this command on your local actions, remote actions or even actions you loaded from a python file.
This is especially useful when you want to change the model of a particular jaseci ai kit module to something else. You can refer the parameters of the setup actions of the module in the docs and then call the setup action with the new parameters.

### Actions Load with context

Normally when you load an action library (Jaseci AI Kit Library), It automatically initialize the model with the default model parameters. But if you want to load the module with different parameters you have to use the `actions call <module_name>.setup -ctx <context>` command. This will load the module with the new parameters. But if you want to override the default parameters of the module you can use the this command.

```bash
jaseci > actions load <module_name> -ctx <context>
```

example using the jac_nlp's gpt2 model to load the model with a different model variant (gpt2-medium) from the default (gpt2) variant, you can use the following command.

```bash
jaseci > actions load jac_nlp.gpt2 -ctx '{"model_name":"gpt2-medium"}'
```