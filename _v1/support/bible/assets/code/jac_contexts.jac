node person {
    has name;
    has age;
    has birthday, profession;
}

edge friend: has meeting_place;
edge family: has kind;

walker init {
    person1 = spawn here -[friend]-> node::person;
    person2 = spawn here -[family]-> node::person;
    person1.name = "Josh"; person1.age = 32;
    person2.name = "Jane"; person2.age = 30;
    e1 = -[friend]->.edge[0];
    e1.meeting_place = "college";
    e2 = -[family]->.edge[0];
    e2.kind = "sister";

    std.out("Context for our people nodes:");
    for i in -->: std.out(i.context);
    # or, for i in -->.node: std.out(i.context);
    std.out("\nContext for our edges to those people:");
    for i in -->.edge: std.out(i.context);
}