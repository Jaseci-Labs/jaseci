node life {
    has anchor owner, note, order, settings;
    can infer.year_from_date;
}

node year {
    has anchor year, note, order;
    can infer.month_from_date;
}

node month {
    has anchor month, note, order;
    can infer.year_from_date;
    can infer.week_from_date;
}

node week {
    has anchor week, note, order;
    can infer.month_from_date;
    can infer.day_from_date;
}

node day {
    has anchor day, note, order, focus_order, ritual_order, expanded_children, focusR;
    has ll_version;
    can infer.day_from_date;
}

node workette {
    has name, order, date, status, snooze_till, color, links, expanded_children;
    has wtype, note, is_MIT, is_ritual;
    has run_start, run_time;
    has goals, sorted_goals;
    has name_emb, name_used_for_emb, note_emb, note_used_for_emb;
}

node summary {
    has all_mit, all_rituals, all_running, all_complete, all_canceled;
}

walker summerizer {
    has start_node;
    summary {
        if(!start_node)
        {
            start_node = here;
            take <--;
        }
    }
    life, year, month, week, day, workette {

    }
}

edge past;
edge parent;

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
            new = spawn here ++> node::year;
            new.year = infer.year_from_date(date);
            take --> node::year == infer.year_from_date(date);
        }
    year: take --> node::month == infer.month_from_date(date) else {
            new = spawn here ++> node::month;
            new.month = infer.month_from_date(date);
            take --> node::month == infer.month_from_date(date);
        }
    month: take --> node::week == infer.week_from_date(date) else {
            new = spawn here ++> node::week;
            new.week = infer.week_from_date(date);
            take --> node::week == infer.week_from_date(date);
        }
    week: take --> node::day == infer.day_from_date(date) else {
            latest_day = spawn here walker::get_latest_day(before_date=date);
            new = spawn here ++> node::day;
            new.day = infer.day_from_date(date);
            if(latest_day) {
                new.order = latest_day.order;
                new.ll_version = latest_day.ll_version;
                spawn latest_day walker::carry_forward(parent=new);
                if new.order: for i=0 to i<new.order.length by i+=1:
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

walker get_workette {
    day, workette {
        report here;
    }
}

walker get_workettes {
    day, workette {
        for i in --> node::workette:
            report i;
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

walker load_workette {
     day, week, month, year, life,  workette {
        for i in  -[parent]-> node::workette {
            report [&here, i];
        }
        take -[parent]-> node::workette;
    }
}

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
        here <+[parent]+ dest_node;
        report here;
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
        take --> ;
        destroy here;
    }
}

walker create_workette {
    has title;
    has wtype, note;
    day, week, month, year, life, workette {
        new = spawn here +[parent]+>
            node::workette(name=title, wtype=wtype, note=note, is_MIT=is_MIT, snooze_till=snooze_till, date=date, is_ritual=is_ritual, color=color);
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
        new_workette = spawn here <+[past]+ node::workette;
        new_workette <+[parent]+ parent;
        new_workette := here;
        if(new_workette.is_ritual): new_workette.status="open";
        spawn -[parent]-> node::workette
            walker::carry_forward(parent=new_workette);
        if new_workette.order: for i=0 to i<new_workette.order.length by i+=1:
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
            spawn here +[parent]+> node::workette(name=rand.sentence());
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

walker update_embeddings {
    can use.get_embedding;
    workette {
        # Update embedding via USE if neccessary
        if ((!here.name_emb && here.name) || (here.name && here.name != here.name_used_for_emb)) {
            here.name_emb = use.get_embedding(here.name);
            here.name_emb = here.name_emb[0];
            here.name_used_for_emb = here.name;
        }

        if ((!here.note_emb && here.note) || (here.note && here.note != here.note_used_for_emb)) {
            here.note_emb = use.get_embedding(here.note);
            here.note_emb = here.note_emb[0];
            here.note_used_for_emb = here.note;
        }
    }
}

walker get_suggested_parent {
    has new_wkt_name, new_wkt_name_emb;
    has cur_best_match, cur_best_score;
    can use.get_embedding;

    with entry {
        cur_best_score = 0.0;
        new_wkt_name_emb = use.get_embedding(new_wkt_name);
        new_wkt_name_emb = new_wkt_name_emb[0];
    }

    day {
        take --> node::workette;
    }

    workette {
        if (here.name == new_wkt_name || here.status == 'done' || here.status == 'canceled'): skip;

        has_children = 0;

        spawn here walker::update_embeddings;

        score_count = 0;
        overall_score = 0.0;

        if (here.name_emb) {
            name_sim = vector.cosine_sim(new_wkt_name_emb, here.name_emb);
            overall_score += name_sim * 0.5;
            score_count += 1;
        }
        if (here.note_emb) {
            note_sim = vector.cosine_sim(new_wkt_name_emb, here.note_emb);
            overall_score += note_sim * 0.5;
            score_count += 1;
        }

        for subwkt in -[parent]-> node::workette {
            spawn subwkt walker::update_embeddings;
            subwkt_vec = [];
            if (subwkt.name_emb): subwkt_vec += [subwkt.name_emb];
            if (subwkt.note_emb): subwkt_vec += [subwkt.note_emb];
            if (has_children == 0) {
                children_embeddings = subwkt_vec;
                has_children = 1;
            } else {
                children_embeddings += subwkt_vec;
            }
        }
        if (has_children == 0 && here.wtype != 'workset') {
            skip;
        }

        if (has_children) {
            centroid = vector.get_centroid(children_embeddings);
            centroid_sim = vector.cosine_sim(new_wkt_name_emb, centroid[0]) * centroid[1];
            overall_score += centroid_sim;
            score_count += 1;
        }

        if (score_count > 0): overall_score /= score_count;

        if (overall_score > cur_best_score) {
            cur_best_match = here;
            cur_best_score = overall_score;
        }
        take -[parent]-> node::workette;
    }

    with exit {
        report [cur_best_match, cur_best_score];
    }
}

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
      if (here.snooze_till) {
        if (infer.date_day_diff(today_date, here.snooze_till) < 0) {
          take -[parent]-> node::workette;
          skip;
        }
      }

      # Select items that are due soon
      if (here.date) {
          if (infer.date_day_diff(here.date, today_date) < soon): due_soon_list += [here];
      }
      take -[parent]-> node::workette;
  }

  with exit {
      if (show_report): report due_soon_list;
  }
}

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
      if (here.snooze_till) {
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

walker init {
    has owner;
    has anchor life_node;
    take (--> node::life == owner) else {
        life_node = spawn here ++> node::life;
        life_node.owner = owner;
        disengage;
    }
}
