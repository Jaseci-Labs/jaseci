---
sidebar_position: 2
---

# Data model

## Nodes

```
node life {
    has anchor owner, note, order, settings;
    can infer.year_from_date;
}
```

`owner` represents the ID of the user who owns the life node. It is used as an anchor here to simplify the representation of life when used in comparisons.

`infer.year_from_date` converts a full date into just the year component.

**From The Docs**

>Nodes, such as life, can also declare actions (similar to walkers). This allows a walker to use the action declared by the node even if it does not declare it itself.

```
node year {
    has anchor year, note, order;
    can infer.month_from_date;
}
```

`year` is a numeric representation of a year, ex: 2021. It is used as an anchor here to simplify the representation of year when used in comparisons.

For example: `if year_node == 2021 ...`

```
node month {
    has anchor month, note, order;
    can infer.year_from_date;
    can infer.week_from_date;
}
```

```
node week {
    has anchor week, note, order;
    can infer.month_from_date;
    can infer.day_from_date;
}
```

`week` is the numeric representation of the weeks of a month, ranging from 1-5


```
node day {
    has anchor day, note, order, focus_order, ritual_order, expanded_children, focusR;
    has ll_version;
    can infer.day_from_date;
}
```

```
node workette {
    has name, order, date, status, snooze_till, color, links, expanded_children;
    has wtype, note, is_MIT, is_ritual;
    has run_start, run_time;
    has goals, sorted_goals;
    has name_emb, name_used_for_emb, note_emb, note_used_for_emb;
}
```

`workette` nodes are the core data type of the application, representing each task or goal and their associated data.

### Edges

```
edge past;
```

![Myca Hierarchy Diagram](/img/tutorial/myca-a-jaseci-product/myca_past_day.png)


The past edge represents the link between:

- A day node and the day node that came before it

- A workette on one day and its "carried forward" copy on another day

>A workette is "carried forward" (or copied) to the next day if it has not yet been completed.

```
edge parent;
```

![Myca Hierarchy Diagram](/img/tutorial/myca-a-jaseci-product/myca_parent_workette.png)

The parent edge represents the link between workettes and child workettes, i.e. tasks and sub-tasks.

>Sub-workettes can go an infinite amount of levels deep (theoretically), i.e. sub-tasks can have sub-tasks.

<!-- TODO: add link from final website -->
Let's move on the [walkers]('#') that will make use of this data model.





