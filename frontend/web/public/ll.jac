node life {
    has anchor owner;
    can infer.year_from_date;
}

node year {
    has anchor year;
    can infer.month_from_date;
}

node month {
    has anchor month;
    can infer.year_from_date;
    can infer.week_from_date;
}

node week {
    has anchor week;
    can infer.month_from_date;
    can infer.day_from_date;
}

node day {
    has anchor day;
    has order, note, ll_version;
    can infer.day_from_date;
}

node workette {
    has name, order, date, status, snooze_till;
    has owner, wtype, note, is_MIT, is_ritual;
}

edge past;
edge parent;

walker get_latest_day {
    has before_date;
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
    }
}

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

walker load_workette {
    day, workette {
        for i in  -[parent]-> node::workette {
            report [&here, i];
        }
        take -[parent]-> node::workette;
    }
}

walker past_to_now {
    has anchor now;
    take <-[past]- else {
        now = here;
    }
}

walker move_workette {
    has dest_node;
    if(!dest_node): disengage;
    workette {
        here !<-[parent]- <-[parent]-;
        here <-[parent]- dest_node;
        report here;
    }
}

walker deep_mits {
    day: take -[parent]-> node::workette;
    workette {
        if(here.is_MIT): report here;
        take -[parent]-> node::workette;
    }
}

walker delete_workette {
    workette {
        take -[parent]-> node::workette;
        destroy here;
    }
}

walker cleanse_all {
    life, root, workette, year, month, week, day {
        take --> node;
        destroy here;
    }
}

walker create_workette {
    has title;
    has wtype;
    day, workette {
        new = spawn here -[parent]-> node::workette(name=title, wtype=wtype);
        report new;
    }
}

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

walker gen_rand_life {
    has num_workettes;
    root {
        take --> node::life else {
            spawn here walker::init();
            take --> node::life;
        }
    }

    life {
        num_workettes = 5;
        num_days = 1; #rand.integer(2, 4);
        for i=0 to i<num_days by i+=1 {
            spawn here walker::get_gen_day(
                date=rand.time("2019-01-01", "2019-12-31")
            );
        }
        take -->;
    }
    year, month, week { take -->; }
    day {
        if(here.day == infer.day_from_date(std.time_now())): skip;
    }
    day, workette {
        if(num_workettes == 0): disengage;
        gen_num = rand.integer(3, 5);
        for i=0 to i<gen_num by i+=1 {
            spawn here -[parent]-> node::workette(name=rand.sentence());
        }
        take --> ;
        num_workettes -= 1;
    }
}

walker init {
    has owner;
    has anchor life_node;
    take (--> node::life == owner) else {
        life_node = spawn here --> node::life;
        life_node.owner = owner;
        disengage;
    }
}
