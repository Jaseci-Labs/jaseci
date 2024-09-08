node person {
    has name="Anon";
}

edge strong;
edge weak;

walker init {
        person1 = spawn here -[strong]-> node::person(name="Joe");
        person2 = spawn here -[strong]-> node::person;
        person3 = spawn here -[weak]-> node::person;
        person4 = spawn here -[weak]-> node::person(name="Mike");

        person1 <--> person2;
        person3 <-[strong]-> person4;

        for i in -->:
            std.out(i.context);
}
