node person {
    has name;
    has byear;
    can set_year with setter entry {
        byear = visitor.year;
    }
    can print_out with exit {
        std.out(byear," from ",visitor.info);
    }
    can reset {  #<-- Could add 'with activity' for equivalent behavior
        byear="1995-01-01";
        std.out("resetting birth year to 1995:", here.context);
    }
}

walker init {
    has year=std.time_now();
    root {
        person1 = spawn here --> node::person;
        std.out(person1);
        person1::reset;
        take --> ;
    }
    person {
        spawn here walker::setter;
        here::reset(name="Joe");
    }
}

walker setter {
    has year=std.time_now();
}