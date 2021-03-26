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
    has anchor name;
    has order, date, owner, status, snooze_till;
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
    for i in  -[parent]-> :
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

walker children_experiment {
  report here;
}

walker get_embedding {
    can use.get_embedding;
    workette {
      here.use_vector_title = use.get_embedding(here.name);
      # here.use_vector_note = use.get_embedding(here.note);
    }
}

walker get_suggested_parent {
    has new_wkt_title;
    has cur_best_match, cur_best_score;
    has children_embeddings;
    has has_children;
    has overall_score;

    can use.get_embedding, bart.eval_assoc;

    day {
      cur_best_score = 0.0;
      new_wkt_title_emb = use.get_embedding(new_wkt_title);
      new_wkt_title_emb = new_wkt_title_emb[0];
      take --> node::workette;
    }

    workette {
      # Re-initialize variables
      has_children = 0;
      
      # Get MNLI score with BART
      title_mnli_score = bart.eval_assoc(new_wkt_title, here.name);
      title_mnli_score = title_mnli_score[0][1];
       
      for subwkt in -[parent]-> node::workette {
        subwkt.use_vector_title = use.get_embedding(subwkt.name);
        if (has_children == 0): children_embeddings = subwkt.use_vector_title;
        else: children_embeddings += subwkt.use_vector_title;
        has_children = 1;
      }
      if (has_children == 1) {
        centroid = vector.get_centroid(children_embeddings);
        centroid_sim = vector.cosine_sim(new_wkt_title_emb, centroid[0]) * centroid[1];
        overall_score = (title_mnli_score + centroid_sim) / 2;
      } else {
        overall_score = title_mnli_score;
      }
      if (overall_score > cur_best_score) {
        cur_best_match = here;
        cur_best_score = overall_score;
      }
      take -[parent]-> node::workette;
    }
    report [cur_best_match, cur_best_score];
}

walker test_walker {
    has children_names;
    has long_name;
    children_names = [];
    long_name = "";
    for wkt in -[parent]-> node::workette {
      children_names += [wkt.name];
    }
    report children_names;
    for cname in children_names {
      long_name += cname;
    } 
    report long_name;
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
