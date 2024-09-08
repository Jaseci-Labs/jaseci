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
    has anchor day, note, order, focus_order, ritual_order, expanded_children, show_hidden_items, focusR, log;
    has ll_version;
    can infer.day_from_date;
}

node workette {
    has name, order, date, status, snooze_till, color, links, expanded_children;
    has wtype, note, is_MIT, is_ritual, is_active;
    has run_start, run_time;
    has name_emb, name_used_for_emb, note_emb, note_used_for_emb;
    has highlight_type;
}

node summary {
    has all_mit, all_rituals, all_running, all_complete, all_canceled;
}

walker push_log {
    has item;
    root, life, year, month, week {
        take net.max(-->);
    }
    day {
        if(not here.log): here.log = [item];
        else: here.log+=[item];
        report here.log;
    }
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
edge associated;
edge highlight;

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

walker delete_day {
    has date;
    if(!date): disengage;
    root: take --> node::life;
    life {
        ignore --> node::year > infer.year_from_date(date);
        take net.max(--> node::year);
    }
    year {
        ignore node::month > infer.month_from_date(date);
        take net.max(--> node::month)
        else {
            ignore here;
            take <-- node::life;
        }
    }
    month {
        ignore node::week > infer.week_from_date(date);
        take net.max(--> node::week)
        else {
            ignore here;
            take <-- node::year == infer.year_from_date(date);
        }
    }
    week {
        ignore node::day > infer.day_from_date(date);
        take net.max(--> node::day)
        else {
            ignore here;
            take <-- node::month == infer.month_from_date(date);
        }
    }
    day {
        spawn --> node::workette walker::delete_workette();
        destroy here;
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
                new.order = [];
                new.expanded_children = latest_day.expanded_children;
                new.focus_order = latest_day.focus_order;
                new.ritual_order = latest_day.ritual_order;
                new.ll_version = latest_day.ll_version;

                spawn latest_day walker::carry_forward(parent=new);

                for i=0 to i<latest_day.order.length by i+=1:
                    new.order += [&(spawn latest_day.order[i] walker::past_to_now)];
                for i=0 to i<new.expanded_children.length by i+=1:
                    new.expanded_children[i] = &(spawn new.expanded_children[i] walker::past_to_now);

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
     day, week, month, year, life,  workette {
        for i in  -[parent]-> node::workette {
            linked = spawn i walker::get_associated;
            report [&here, i, linked];
        }

        take -[parent]-> node::workette;
    }
}

walker get_associated {
    has anchor associated;
    with entry {
        associated = [];
    }
    workette {
        associated = <-[associated]->;
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
    has dest_node, dest_node_order, src_node, src_node_order;
    if(!dest_node): disengage;
    workette {
        here !<-[parent]- <-[parent]-;
        here <+[parent]+ dest_node;

        if(src_node_order && src_node): src_node_order = src_node_order;
        if(dest_node_order): dest_node.order = dest_node_order;

        report here;
    }
}

walker link_with_goal {
    has goal_node;
    if(!goal_node): disengage;
    workette {
        here !<-[associated]-> <-[associated]->;
        here <+[associated]+> goal_node;
        report here;
    }
}

walker unlink_goal {
    workette {
        here !<-[associated]-> <-[associated]->;
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
    has title, wtype, note, is_MIT, snooze_till, date, is_ritual, color;

    day, week, month, year, life, workette {
        new = spawn here +[parent]+>
            node::workette(name=title, wtype=wtype, note=note, is_MIT=is_MIT, snooze_till=snooze_till, date=date, is_ritual=is_ritual, color=color);
        report new;
    }
}

walker carry_forward {
    # parent = new day/workette
    # here = current/previous day/workette
    has parent;
    day {
        here <+[past]+ parent;
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
        new_workette.order = [];
        for i=0 to i<here.order.length by i+=1:
            new_workette.order += [&(spawn here.order[i]
                                      walker::past_to_now)];
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

walker gen_day_workettes {
    has date;
    has num_workettes;

    with_entry {
        if(!num_workettes): num_workettes = 0;
    }

    root {
        spawn here walker::delete_day(date=date);

        take --> node::life else {
            spawn here walker::init();
            take --> node::life;
        }
    }

    life {
        spawn here walker::get_gen_day(date=date);
        take -->;
    }
    year, month, week { take -->; }
    day {
        if(num_workettes == 0): disengage;

        for i=0 to i<num_workettes by i+=1 {
            day_workettes = spawn here walker::get_workettes_deep;
            #std.log(day_workettes);
            if( day_workettes.length > 0 ) {
                rand_int = rand.integer(0, day_workettes.length - 1);
                parent = day_workettes[rand_int];
            }
            else: parent = &here;

            #std.log(parent);

            spawn *parent walker::create_workette(title=rand.sentence(), wtype="workette");
        }

        #spawn here walker::get_workettes_deep(show_report=true);
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
    has dummy;
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
        if (here.name == new_wkt_name || here.wtype != 'workset' || here.status == 'done' || here.status == 'canceled'): skip;

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
            centroid_sim = vector.cosine_sim(new_wkt_name_emb, centroid[0]);
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
      # ignore already starred and workset
      if (here.is_MIT || here.wtype == 'workset') {
          take -[parent]-> node::workette;
          skip;
      }
      # ignore item that is currently snoozed
      if (here.snooze_till && here.snooze_till != '') {
        if (infer.date_day_diff(today_date, here.snooze_till) < 0) {
          take -[parent]-> node::workette;
          skip;
        }
      }

      # Select items that are due soon
      if (here.date && here.date != '') {
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
      if (here.is_MIT || here.wtype == 'workset') {
          take -[parent]-> node::workette;
          skip;
      }
      # Select items that are snoozed until today or recent past days
      if (here.snooze_till && here.snooze_till != '') {
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
      if (!max_items): max_items = 5;
  }

  day {
      report_cnt = 0;
      due_soon_list = spawn here walker::get_due_soon(soon=soon_delta);
      for i=0 to i<due_soon_list.length by i+=1 {
          report [due_soon_list[i], 'Due soon.'];
          report_cnt += 1;
          if (report_cnt == max_items): disengage;
      }

      snooze_list = spawn here walker::get_snoozed_till_recent;
      for i=0 to i<snooze_list.length by i+=1 {
          report [snooze_list[i], 'Snoozed until recent.'];
          report_cnt += 1;
          if (report_cnt == max_items): disengage;
      }
      # TODO: This takes way too long right now. Need to optimize this and then bring it back.
      # old_list = spawn here walker::get_long_active_items(long_days=long_days);
      # for i=0 to i<old_list.length by i+=1 {
      #     report [old_list[i], 'Outstanding for more than a week.'];
      #     report_cnt += 1;
      #     if (report_cnt == max_items): disengage;
      # }
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

# Clear any highlight set for this workette
# Also clear any highlight edges
walker clear_highlight {
    workette {
        here.highlight_type = 0;
        here !<-[highlight]-> <-[highlight]->;
    }
}

# Set highlight for a given workette
# Create a highlight edge between the wkt and day node
walker set_highlight {
    has highlight_type;
    has this_workette, if_set;

    with entry {
        if_set = false;
    }

    workette {
        if (if_set) {
            # keep walking up the graph to find today's day node
            take <-[parent]-;
            skip;
        }

        # set the highlight type
        here.highlight_type = highlight_type;
        if_set = true;
        this_workette = here;

        # walk up the graph to find today's day node
        take <-[parent]-;
    }

    day {
        here +[highlight]+> this_workette;
        report this_workette;
        disengage;
    }
}

walker clear_day_highlight {
    day {
        take -[highlight]->;
    }

    workette {
        here.highlight_type = "";
        here !<-[highlight]- <-[highlight]-;
    }
}

walker set_day_highlight {
    has highlight_items;
    has dayNode;
    has types;
    has cnt;

    with entry {
        cnt = 0;
    }

    day {
        if( !highlight_items ): disengage;

        #clear highlights
        spawn here walker::clear_day_highlight;

        types = [];

        dayNode = here;

        for h in highlight_items {
            typeObj = {"type": h["type"], "color": h["color"], "icon": h["icon"]};

            types += [typeObj];

            if( h["id"] ): take *(h["id"]);
        }
    }

    workette {
        here.highlight_type = types[cnt];
        here <+[highlight]+ dayNode;

        cnt += 1;
    }

    with exit {
        spawn dayNode walker::get_highlights(num_days_to_load=1);
    }
}

walker get_highlights {
    has page;
    has num_days_to_load;
    has loaded_days;
    has anchor highlights;
    with entry {
        highlights = [];
        loaded_days = 0;

        if(!num_days_to_load): num_days_to_load = 7;
    }

    day {
        items = [];
        if (loaded_days == num_days_to_load) {
            disengage;
        }

        for w in -[highlight]-> {
            items += [{"id": &(w), "type": w.highlight_type["type"], "color": w.highlight_type["color"], "icon": w.highlight_type["icon"], "item": w.name}];
        }

        highlights += [[[here, here.day], here.note, items]];

        loaded_days += 1;

        take -[past]->;
    }

    with exit {
        report [highlights, 1];
    }
}

# for testing
walker get_workettes {
    has show_report;
    has anchor lst;

    with entry {
        lst = [];
    }

    day, workette {
        for i in --> node::workette:
            lst += [i];
    }

    with exit {
        if( show_report ): report lst;
    }
}

walker get_workettes_deep {
    has show_report;
    has anchor lst;

    with entry {
        lst = [];
    }

    day {
        take --> node::workette;
    }
    workette {
        lst += [&here];
        take --> node::workette;
    }

    with exit {
        if( show_report ): report lst;
    }
}

node deep: has d={"a": {"b": {"c": [5]}}};

walker check_deep_write_start { a=spawn here ++> n::deep;}

walker check_deep_write_update {
    take --> n::deep;
    deep {
        here.d["a"]['b']['c'].l::append(6);
    }
}

walker check_deep_write_report {
    take --> n::deep;
    deep {
        report here.d;
    }
}