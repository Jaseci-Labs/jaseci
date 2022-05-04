---
sidebar_position: 1
---

# How Extensions Work

Extensions allow a developer to extend the functionality and add new capabilities to Jaseci and the Jac standard library.

In this section we will explain how to use extensions by making use of actions already built-in, and then cover how to create your own extensions.

Extensions (or actions) are predefined functions that a walker can make use of to perform an operation. The actions a walker can use are either scoped or global. Scoped actions must be declared using the can keyword before they are accessible. Conversely, global actions are accessible without a declaration. A full list of built-in actions can be found here.

### Using the can keyword in a scoped action declaration

Here, the `infer_from_date` action from the `infer` module is declared as a capability of the `date_get_year` walker. This action is then used later on in the walker body definition.

```jac
walker date_get_year {
    has date;
    can infer.year_from_date;

    report infer.year_from_date(date);
}
```

### Using a global action

Since the `rand` module is global its actions are accessible without a declaration.

```jac
walker get_random_int {    
    report rand.integer(0, 10);
}
```

>Extensions are typically scoped actions that provide some additional functionality through custom logic and/or connecting to an external service.

### Using an action that connects to an external AI service

```jac
walker infer_best_topic {
    has topics;
    has anchor best_topic;  # used as return value
    has sentence;           # used as parameter

    can use.get_embedding;  # this scoped action connects to an external service

    with entry {
        topics = ['Sports', 'Finance', 'Education', 'Entertainment'];
    }

    best_score = 0.0;
    sentence_emb = (use.get_embedding(sentence))[0];
    for t in topics {
        t_emb = (use.get_embedding(t))[0];
        score = vector.cosine_sim(t_emb, sentence_emb); # use of another global build-in action
        if score > best_score {
            best_score = score;
            best_topic = t;
        }
    }

    report best_topic;
}
```