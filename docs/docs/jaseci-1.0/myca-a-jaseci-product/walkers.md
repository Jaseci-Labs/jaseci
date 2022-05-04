---
sidebar_position: 3
---

# Walkers

First, we'll take a look at the simple walkers that make up myca.

## Initialization

`init` looks for an instance of the graph for the current user (`owner`) and creates one if it does not exist.

```jac
walker init {
    has owner;
    has anchor life_node;
    take (--> node::life == owner) else {
        life_node = spawn here --> node::life;
        life_node.owner = owner;
        disengage;
    }
}
```

## Workette manipulation

`get_workette` reports the current workette or day node.

```jac
walker get_workette {
    day, workette {
        report here;
    }
}

```

`get_workettes` reports all the immediate child workettes on a day or workette node.

```jac
walker get_workettes {
    day, workette {
        for i in --> node::workette:
            report i;
    }
}
```

`get_workettes_deep` reports all workettes and sub-workettes on a day node

```jac
walker get_workettes_deep {
    day {
        take --> node::workette;
    }
    workette {
        report here;
        take --> node::workette;
    }
}
```

`load_workette` reports a tuple for all workettes and sub-workettes on a node along with the id of that node.

```jac
walker load_workette {
     day, week, month, year, life,  workette {
        for i in  -[parent]-> node::workette {
            report [&here, i];
        }
        take -[parent]-> node::workette;
    }
}
```

`create_workette` takes in the parameters necessary to create a workette and spawns a new one on the current node.

```jac
walker create_workette {
    has title;
    has wtype, note;
    day, week, month, year, life, workette {
        new = spawn here -[parent]->
            node::workette(name=title, wtype=wtype, note=note, is_MIT=is_MIT, snooze_till=snooze_till, date=date, is_ritual=is_ritual, color=color);
        report new;
    }
}
```

**From The Docs**
>Nodes can take arguments when being spawned. These arguments set the node's properties to the values passed to the constructor.

`move_workette` moves a workette from one node to another by using edge manipulation.

```jac
walker move_workette {
    has dest_node;
    if(!dest_node): disengage;
    workette {
        here !<-[parent]- <-[parent]-;
        here <-[parent]- dest_node;
        report here;
    }
}

```

**From The Docs**
> Edges can be deleted using the ! operator to negate the linking procedure.

`delete_workette` deletes a workette node.

```jac
walker delete_workette {
    workette {
        take -[parent]-> node::workette;
        destroy here;
    }
}
```

*** From The Docs**
Use the `destroy` keyword to delete a node.

## Date component manipulation

<!-- TODO: add link below -->
`get_gen_day` looks for a day node that matches the date parameter or creates one and reports it. [see advanced walkers](/docs/myca-a-jaseci-product/walkers-advanced)

`get_*` walks the graph looking for the respective date component node (`week`, 'month', etc) that matches the `date` parameter and reports it and its workettes.

```jac
walker get_week {
    has date;
    if(date){
        root: take --> node::life;
        life: take --> node::year == infer.year_from_date(date);
        year: take --> node::month == infer.month_from_date(date);
        month: take --> node::week == infer.week_from_date(date);
        week {
            report [ "", here ];
            spawn here walker::load_workette;
        }
    }
}
```

```jac
walker get_month {
        has date;
    if(date){
        root: take --> node::life;
        life: take --> node::year == infer.year_from_date(date);
        year: take --> node::month == infer.month_from_date(date);
        month {
            report [ "", here ];
            spawn here walker::load_workette;
        }
    }
}
```

```jac
walker get_year {
        has date;
    if(date){
        root: take --> node::life;
        life: take --> node::year == infer.year_from_date(date);
        year {
            report [ "", here ];
            spawn here walker::load_workette;
        }
    }
}
```

```jac
walker get_life {
        has date;
    if(date){
        root: take --> node::life;
        life {
            report [ "", here ];
            spawn here walker::load_workette;
        }
    }
}
```
