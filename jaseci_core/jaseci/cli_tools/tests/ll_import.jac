import {*} with "./ll_base.jac";

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
