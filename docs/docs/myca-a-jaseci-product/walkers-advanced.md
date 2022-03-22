---
sidebar_position: 4
---

# Walkers - Advanced

Now for a bit more complex walkers. These use advanced language features or have somewhat complex logic to them.

`get_gen_day` walks the graph looking for a day node that represents the `date` property (typically the current date). It does this by checking for the nodes that match each component of the `date` parameter then traversing down the path of matching nodes.

Things to note:

<!-- TODO: Add link below -->
- At each level it creates the required node that corresponds with each date component if it does not exist (life -> year -> etc..).
- On the `week` node, in addition to spawning a new `day` if a matching one doesn't exist, it checks for the most recent previous day using `get_latest_day` (learn more) and copies all incomplete workettes to the new day using `carry_forward` [learn more](/docs/intermediate/standard-library-documentation/jaseci-primitives#walker).

```jac
walker get_gen_day {
    has date;
    has anchor day_node;
    if(!date): date=std.time_now();
    root {
        take --> node::life else {
            spawn here walker::init();
            take --> node::life;
        }
    }
    life: take --> node::year == infer.year_from_date(date) else {
            new = spawn here --> node::year;
            new.year = infer.year_from_date(date);
            take --> node::year == infer.year_from_date(date);
        }
    year: take --> node::month == infer.month_from_date(date) else {
            new = spawn here --> node::month;
            new.month = infer.month_from_date(date);
            take --> node::month == infer.month_from_date(date);
        }
    month: take --> node::week == infer.week_from_date(date) else {
            new = spawn here --> node::week;
            new.week = infer.week_from_date(date);
            take --> node::week == infer.week_from_date(date);
        }
    week: take --> node::day == infer.day_from_date(date) else {
            latest_day = spawn here walker::get_latest_day(before_date=date);
            new = spawn here --> node::day;
            new.day = infer.day_from_date(date);
            if(latest_day) {
                new.order = latest_day.order;
                new.ll_version = latest_day.ll_version;
                spawn latest_day walker::carry_forward(parent=new);
                for i=0 to i<new.order.length by i+=1:
                    new.order[i] = &(spawn new.order[i] walker::past_to_now);
                take new;
            }
            else: take new;
        }
    day {
        day_node = here;
        report [ "", here ];
        spawn here walker::load_workette;
    }
}
```

**From The Docs**
>You can `take` a specific instance of a node.
>Example: `monday = spawn here node::day; take monday;`


### Walker: get_latest_day

`get_latest_day` returns the most recent day that comes before the `before_date` property. It does this by walking the graph with conditions to `ignore` nodes that represent a time past `before_date`, then taking the most recent of the remaining nodes for each date component.

Things to note:

- On the `year`, `month`, and `week` nodes, if no usable children are found it goes back up one level with take `<-- ...` so the next instance of the the node can be checked.

```jac
walker get_latest_day {
    has before_date, show_report;
    has anchor latest_day;
    if(!before_date): before_date = std.time_now();
    if(!latest_day): latest_day = 0;
    root: take --> node::life;
    life {
        ignore --> node::year > infer.year_from_date(before_date);
        take net.max(--> node::year);
    }
    year {
        ignore node::month > infer.month_from_date(before_date);
        take net.max(--> node::month)
        else {
            ignore here;
            take <-- node::life;
        }
    }
    month {
        ignore node::week > infer.week_from_date(before_date);
        take net.max(--> node::week)
        else {
            ignore here;
            take <-- node::year == infer.year_from_date(before_date);
        }
    }
    week {
        ignore node::day > infer.day_from_date(before_date);
        take net.max(--> node::day)
        else {
            ignore here;
            take <-- node::month == infer.month_from_date(before_date);
        }
    }
    day {
        latest_day = here;
        if(show_report) {
            report [ "", here ];
            spawn here walker::load_workette;
        }
    }
}
```

### Walker: carry_forward

`carry_forward` is used to copy incomplete workettes from the most recent previous day to the current day. For each workette, this involves spawning a new one with a past edge to the one being copied, creating a `parent` edge to the new day being passed in as the `parent` property, copying all properties of the old workette, and making a recursive call to `carry_forward` to handle copying sub-workettes in a similar way.

Things to note:

- The recursive call to `carry_forward` spawns it on a collection of nodes that match the filter or query set (`-[parent]-> node::workette`), rather than just a single node.

```jac
walker carry_forward {
    has parent;
    day {
        take -[parent]-> node::workette;
    }
    workette {
        if(!(here.is_ritual) and
           (here.status == 'done' or
            here.status == 'canceled')): skip;
        new_workette = spawn here <-[past]- node::workette;
        new_workette <-[parent]- parent;
        new_workette := here;
        if(new_workette.is_ritual): new_workette.status="open";
        spawn -[parent]-> node::workette
            walker::carry_forward(parent=new_workette);
        for i=0 to i<new_workette.order.length by i+=1:
            new_workette.order[i] = &(spawn new_workette.order[i]
                                      walker::past_to_now);
    }
}
```

**From The Docs**

Use the `:=` operator to copy properties from one node to another.

You can spawn a walker on a collection of filtered nodes.

Ex: `-[parent]-> node::workette` represents a collection of nodes connected by the `parent` edge, of the `workette` node type.

### Walker: past_to_now

`past_to_now` returns the latest version of a node that uses the `past` edge. It does this by traversing all `past` edges that point towards the current node until there are none left. At that point it ends up at the most recent version of the node.

Things to note:

- We traverse against the defined direction of the `past` edge to get to the latest node. See [myca edges](/docs/myca-a-jaseci-product/data-model#edges).

```jac
walker past_to_now {
    has anchor now;
    take <-[past]- else {
        now = here;
    }
}
```

**From The Docs**


>Edge definition directionality does not limit traversal direction.

>Use `take <--` to traverse edges that **point towards** the current node.

>Use `take -->` to traverse edges that **point away from** the current node.

>... regardless of the directionality of the edge.

### Walker: get_suggested_focus

`get_suggested_focus` reports a collection of recommended workettes that need attention. This may include workettes where the due date is nearby, the snooze has expired recently or will expire on the current day, and ones that have been incomplete and copied over many days.

For details on how each of the criteria are determined see walkers [get_due_soon](/docs/myca-a-jaseci-product/walkers-advanced#walker-get_due_soon), [get_snoozed_till_recent](/docs/myca-a-jaseci-product/walkers-advanced#walker-get_snoozed_till_recent), and [get_long_active_items](/docs/myca-a-jaseci-product/walkers-advanced#walker-get_long_active_items).

```jac
walker get_suggested_focus {
  has max_items, long_days, soon_delta;

  with entry {
      if (!long_days): long_days = 7;
      if (!soon_delta): soon_delta = 3;
  }

  day {
      suggested = [];
      suggested += spawn here walker::get_due_soon(soon=soon_delta);
      suggested += spawn here walker::get_snoozed_till_recent;
      if (suggested.length >= max_items) {
          report suggested;
          disengage;
      }
      old_list = spawn here walker::get_long_active_items(long_days=long_days);
      cur_cnt = suggested.length;
      for i=cur_cnt to i<max_items by i+=1 {
          lidx = i - cur_cnt;
          if (lidx == old_list.length) {
              report suggested;
              disengage;
          }
          old_item = old_list[lidx];
          suggested += [old_item];
      }
      report suggested;
  }
}
```

**From the docs**

>Use `disengage` to stop walker execution on all instances of a node type immediately.

## Walker: get_due_soon

`get_due_soon` reports the workettes that have an upcoming due date that is close to the current date. The number of days the due date has to be away from the current date is specified by the `soon` parameter. It also skips special workette types and any snoozed workettes.

```jac
walker get_due_soon {
  has soon, show_report;
  has anchor due_soon_list, today_date;
  can infer.date_day_diff;

  with entry {
      due_soon_list = [];
      today_date = infer.day_from_date(std.time_now());
  }

  day {
      take -[parent]-> node::workette;
  }

  workette {
      # ignore workset
      if (here.wtype == 'workset') {
          take -[parent]-> node::workette;
          skip;
      }
      # ignore item that is currently snoozed
      if (here.snooze_till != '') {
        if (infer.date_day_diff(today_date, here.snooze_till) < 0) {
          take -[parent]-> node::workette;
          skip;
        }
      }

      # Select items that are due soon
      if (here.date != '') {
          if (infer.date_day_diff(here.date, today_date) < soon): due_soon_list += [here];
      }
      take -[parent]-> node::workette;
  }

  with exit {
      if (show_report): report due_soon_list;
  }
}
```

**From The Docs**
>Use `skip` to stop walker execution on the current instance of a node type immediately.

### Walker: get_snoozed_till_recent

`get_snoozed_till_recent` looks for workettes where the snooze has expired recently or will expire today.

```jac
walker get_snoozed_till_recent {
  has show_report;
  has anchor snoozed_to_active_list;
  has today_date;
  can infer.date_day_diff;

  with entry {
      snoozed_to_active_list = [];
      today_date = infer.day_from_date(std.time_now());
  }

  day {
      take -[parent]-> node::workette;
  }

  workette {
      # ignore workset
      if (here.wtype == 'workset') {
          take -[parent]-> node::workette;
          skip;
      }
      # Select items that are snoozed until today or recent past days
      if (here.snooze_till != '') {
          if (infer.date_day_diff(today_date, here.snooze_till) > 0) {
              snoozed_to_active_list += [here];
          }
      }
      take -[parent]-> node::workette;
  }

  with exit {
      if (show_report): report snoozed_to_active_list;
  }
}
```

### Walker: get_long_active_items

`get_long_active_items` looks for workettes that have been incomplete over many days (specified by the `long_days` parameter) by counting the number of times it has been carried forward through the `past` edge.
<!-- TODO: Add link below -->
See [days_in_backlog](/docs/myca-a-jaseci-product/walkers-advanced#walker-days_in_backlog) for more details.

```jac
walker get_long_active_items {
  has long_days, show_report;
  has anchor old_list;

  with entry {
      if (!long_days): long_days = 7;
      old_list = [];
  }

  day {
      take -[parent]-> node::workette;
  }

  workette {
      # only consider workettes
      if (here.wtype == 'workset') {
          take -[parent]-> node::workette;
          skip;
      }
      # Select items that have been in backlog for more than a week
      num_days = spawn here walker::days_in_backlog;
      if (num_days >= long_days): old_list += [[here, num_days]];

      take -[parent]-> node::workette;
  }

  with exit {
      # sort old workettes
      old_list = vector.sort_by_key(old_list, 1, 1);
      if (show_report): report old_list;
  }
}
```

### Walker: days_in_backlog

`days_in_backlog` counts the number of times a workette has been carried forward by traversing through the past edge and counting the number of links.

```jac
walker days_in_backlog {
    has show_report;
    has anchor num_days;

    with entry {
      num_days = 0;
    }
    workette {
      num_days += 1;
      take -[past]-> node::workette else {
          if (show_report): report num_days;
      }
    }
}
```