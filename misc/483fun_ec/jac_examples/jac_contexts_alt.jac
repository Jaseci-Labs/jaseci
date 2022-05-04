node person: has name, age, birthday, profession;
edge friend: has meeting_place;
edge family: has kind;

walker init {
    person1 = spawn here -[friend(meeting_place = "college")] ->
        node::person(name = "Josh", age = 32);
    person2 = spawn here -[family(kind = "sister")] ->
        node::person(name = "Jane", age = 30);

    std.out("Context for our people nodes and edges:");
    for i in -->: std.out(i.context, '\n', i.edge[0].context);
}