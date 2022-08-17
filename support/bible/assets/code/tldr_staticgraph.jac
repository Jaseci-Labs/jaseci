node person {
    has name="Anon";
}

edge strong;
edge weak;

graph basic_gph {
    has anchor root;
    spawn {
        root = spawn node::generic;
        person1 = spawn root -[strong]-> node::person(name="Joe");
        person2 = spawn root -[strong]-> node::person;
        person3 = spawn root -[weak]-> node::person;
        person4 = spawn root -[weak]-> node::person(name="Mike");

        person1 <--> person2;
        person3 <-[strong]-> person4;
    }

}

walker init {
    spawn here --> graph::basic_gph;
    spawn here --> graph::basic_gph;
    spawn here --> graph::basic_gph;
}