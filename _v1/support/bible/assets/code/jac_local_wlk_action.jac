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
        ::set_back_to_95;
        std.out("resetting year to 1995:", here.context);
    }
    can set_back_to_95: byear="1995-01-01";
}

walker init {
    has year=std.time_now();
    can setup {
        person1 = spawn here ++> node::person;
        std.out(person1);
        person1::reset;
    }
    root {
        ::setup;
        take --> ;
    }
    person {
        spawn here walker::setter;
        person1::reset(name="Joe");
    }
}

walker setter {
    has year=std.time_now();
}