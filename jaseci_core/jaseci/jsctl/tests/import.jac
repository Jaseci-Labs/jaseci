walker init {
    has year = std.time_now();
    has person1;
    root {
        person1 = spawn here --> node::person;
        report person1.context;
        person1::reset;
        take -->;
    }
    person {
        spawn here walker::setter;
        person1::reset(name="Joe");
    }
}

global say = "resetting year to 1995:";

walker setter {
    has year = std.time_now();
}