ll_proto = \
    """
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
    }

    node workette {
        has name, order, date, owner, status, snooze_till;
        has note, is_MIT, is_ritual;
    }

    edge past;

    edge parent;

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
        if(!latest_day): latest_day = 0;

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
            take --> node::workette;
        }
        workette {
            report here;
            take --> node::workette;
        }
    }

    walker get_sub_workettes {
        report here;
        workette: take --> node::workette;
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
            num_workettes = 10;
            num_days = rand.integer(2, 4);
            for i=0 to i<num_days by i+=1 {
                spawn here walker::get_gen_day(
                    date=rand.time("2019-01-01", "2019-12-31")
                );
            }
            take -->;
        }
        year, month, week { take -->; }
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


    """

prog3 = \
    """
    has date;
    node life {
    }

    walker init {
        new = spawn here --> node::life;
        root.date = std.time_now();
        banana = std.log(root.date);
    }
    """

prog0 = \
    """
    node test:0 {
        has a, b, c;
        can std.log::a,b::>c with exit;
    }

    walker test {
        test {
            here.a = 43;
            here.b = 'Yeah \\n"fools"!';
            report here.b;
            if(4 > 6) { std.log("a"); }
            elif(5>6) { std.log("b"); }
            elif(6>6) { std.log("c"); }
            elif(7>6) { std.log(576); }
        }
    }

    node life:0 {
    }

    node year {
        has anchor year;

    }

    walker another {
        life {
            here.a = 43;
            here.b = 'Yeah \\n"fools"!';
            report here.b;
            if("4 > 6" == "4 > 6") { std.log("a"); }
        }
    }
    """

prog1 = \
    """
    node test:0 {
        has a, b, c;
        can std.log::a,b::>c with exit;
    }

    walker test {
        test {
            here.a = 43;
            here.b = 'Yeah \\n"fools"!';
            report here.b;
            if(4 > 6) { std.log("a"); }
            elif(5>6) { std.log("b"); }
            elif(6>6) { std.log("c"); }
            elif(7>6) { std.log(576); }
        }
    }

    node life:0 {
    }

    node year {
        has anchor year;

    }

    node month {
        has anchor month;
    }

    node week {
        has anchor week;
    }

    node day {
        has anchor day;
    }

    node workette {
        has date, owner, status, snooze_till;
        has note, is_MIT, is_ritual;
    }

    walker use_test {
        can use.enc_question, use.enc_answer, use.qa_dist;
        has output;
        q = use.enc_question(["How old are you?", "which animal is the best?"]);
        a = use.enc_answer(["I'm 40 years old.", "Elephants rule."]);
        output=use.qa_dist(q, a);
    }

    walker get_day {
        has date;
        life: take infer.year_from_date(date);
        year: take infer.month_from_date(date);
        month: take infer.week_from_date(date);
        week: take infer.day_from_date(date);
        day: report --> ;
    }

    walker get_gen_day {
        has date;
        can infer.year_from_date;
        can infer.month_from_date;
        can infer.week_from_date;
        can infer.day_from_date;
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
                new = spawn here --> node::day;
                new.day = infer.day_from_date(date);
                take --> node::day == infer.day_from_date(date);
            }
        day: report --> ;
    }

    walker get_sub_workettes {
        workette: report --> node::workette;
    }

    walker get_latest_day {
        life: take year.max_outbound;
        year: take month.max_outbound;
        month: take week.max_outbound;
        week: report day.max_outbound;
    }

    walker carry_forward {
        has my_root;
        day {
            new_day = spawn here --> node::day;
            my_root = new_day;
            take day.outbound_nodes;
        }
        workette {
            if(workette.status == 'done' or
            workette.status == 'eliminated') {
                continue;
            }
            childern = workette.outbound_nodes;
            new_workette = spawn here --> node::workette;
            parent = me.spawn_history.last(-1);
            new_workette <-- parent;
            take --> node::workette;
        }
        report me.spawn_history;
        report new_day;
    }
    """
