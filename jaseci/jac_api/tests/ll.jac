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
    has ll_version;
    can infer.day_from_date;
}

node workette {
    has name, order, date, owner, status, snooze_till;
    has note, is_MIT, is_ritual;
    has goals, sorted_goals;
    has use_vector_title, use_vector_note;
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
        report here;
    }
}

walker get_gen_day {
    has date;
    has anchor day_node;
    if(!date): date=std.time_now();
    root: take --> node::life;
    life: take --> node::year == infer.year_from_date(date) else {
            new = spawn here --> node::year ;
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
            latest_day = spawn here walker::get_latest_day;
            new = spawn here --> node::day;
            new.day = infer.day_from_date(date);
            if(latest_day and infer.day_from_date(date) ==
                infer.day_from_date(std.time_now())) {
                spawn latest_day walker::carry_forward(parent=new);
                take new;
            }
            elif(latest_day) {
                take latest_day;
            }
            else: take new;
        }
    day {
        day_node = here;
        report here;
    }
}

walker get_workettes {
    day, workette {
        for i in  --> node::workette:
            report i;
    }
}

walker get_workette {
    day, workette {
        report here;
    }
}

walker delete_workette {
    workette {
        take --> node::workette;
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
    day, workette {
        new = spawn here -[parent]-> node::workette;
        report new;
    }
}
walker create_workette_with_title {
    has title;
    day, workette {
        new = spawn here -[parent]-> node::workette(name=title);
        report new;
    }
}
walker get_workettes_deep {
    day {
        take --> node::workette;
    }
    workette {
        report here;
        take --> node::workette;
    }
}

walker get_children {
    for i in  --> :
        report i;
}

walker carry_forward {
    has parent;
    day {
        take --> node::workette;
    }
    workette {
        if(here.status == 'done' or
        here.status == 'eliminated') {
            disengage;
        }
        new_workette = spawn here <-[past]- node::workette;
        new_workette <-[parent]- parent;
        new_workette := here;
        spawn --> node::workette
            walker::carry_forward(parent=new_workette);
    }
}

walker gen_rand_life {
    has num_workettes;
    root: take --> node::life;

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


walker eval_relevance {
    has new_wkt_title, new_wkt_title_emb;
    can bart.eval_assoc;
    can use.get_embedding;
      
    workette {
      if (here.use_vector_title == None):
        here.use_vector_title = use.get_embedding(here.title);
      if (here.use_vector_note == None):
        here.use_vector_note = use.get_embedding(here.note);

      title_mnli_score = bart.eval_assoc(new_wkt_title, here.title)[1];
      note_sim_score = cosine_sim(new_wkt_title_emb, here.note);

      num_children = 0
      childrens = []
      for sub_wkt in take --> node::workette {
        num_children += 1
        childrens.append(spawn here walker::eval_relevance)
      }
      if (num_children == 0) {
        report [here, title_mnli_score, note_sim_score, 0]
      } else {
      }

    }
}
walker get_suggested_parent {
    has new_wkt_title;
    can bart.eval_assoc;
    can use.get_embedding;

    has candidates;

    take (<-- node::day) {
      for wkt in --> node::workette :
        bart_score = bart_eval_assoc(new_wkt_title, wkt.title)[1];
    }
}


walker add_and_associate_goals {
    has goals;
    can bart.eval_assoc;
    workette {
        if(here.goals == goals): disengage;
        here.sorted_goals = bart.eval_assoc(here.name, goals);
        here.goals = goals;
        report here;
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
