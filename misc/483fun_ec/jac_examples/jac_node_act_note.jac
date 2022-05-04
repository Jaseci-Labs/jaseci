node person {
    has name;
    has birthday;
    can date.quantize_to_year with activity;  # <-- walkers can call
}

walker init {
    root {
        person1 = spawn here -->
            node::person(name="Josh", birthday="1995-05-20");
        take -->;
    }
    person {
        birthyear = date.quantize_to_year(here.birthday);
        std.out(birthyear);
    }
}