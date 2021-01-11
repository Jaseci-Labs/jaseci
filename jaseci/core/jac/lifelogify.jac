node life {
    has owner;
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
}

node workette {
    has order, date, owner, status, snooze_till;
    has note, is_MIT, is_ritual;
}

walker get_day {
    has date;
    life: take --> node::year == infer.year_from_date(date);
    year: take --> node::month == infer.month_from_date(date);
    month: take --> node::week == infer.week_from_date(date);
    week: take --> node::day == infer.day_from_date(date);
    day: report here;
    report false;
}

walker get_latest_day {
    has before_date;
    has anchor latest_day;
    if(!before_date): before_date = std.time_now();

    life {
        ignore node::year > infer.year_from_date(before_date);
        take --> node::year == net.max()
        else {
            report false;
        }
    }
    year {
        ignore node::month > infer.month_from_date(before_date);
        take --> node::month == net.max()
        else {
            ignore here;
            take <-- node::life == net.first();
        }
    }
    month {
        ignore node::week > infer.week_from_date(before_date);
        take --> node::week == net.max()
        else {
            ignore here;
            take <-- node::year == infer.year_from_date(before_date);
        }
    }
    week {
        ignore node::day >= infer.day_from_date(before_date);
        take --> node::day == net.max()
        else {
            ignore here;
            take <-- node::month == infer.month_from_date(before_date);
        }
    }
    day {
        my.latest_day = here;
        report here;
    }
}

walker get_gen_day {
  	date = std.time_now();
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
            spawn latest_day walker::carry_forward(parent=new);
            new.day = infer.day_from_date(date);
            take --> node::day == infer.day_from_date(date);
        }
    day: report here;
}

walker get_sub_workettes {
    report here;
    workette: take --> node::workette;
}

walker carry_forward {
    has parent;
    day {
        take node::workette;
    }
    workette {
        if(workette.status == 'done' or
        workette.status == 'eliminated') {
            stop;
        }
        new_workette = --> node::workette;
        new_workette = here;
        new_workette <-- parent with edge::parent;
        new_workette <-- here with edge::past;
        spawn --> node::workette
            walker::get_carry_forward(parent=new_workette);
    }
}

walker init {
    new = spawn here --> node::life;
}
