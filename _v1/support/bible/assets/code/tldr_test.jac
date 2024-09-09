node person: has name="Anon";

graph basic {
    has anchor root;
    spawn {
        root = spawn node::generic;
        person1 = spawn root --> node::person(name="Joe");
        person2 = spawn root --> node::person;
        person3 = spawn root --> node::person;
        person4 = spawn root --> node::person(name="Mike");
        person1 <--> person2;
        person3 <--> person4;
    }

}

walker tally {
    has count=0, visited=[];
    count += 1;

    if(here not in visited) {
        visited.l::append(here);
        take -->;
    }
}

test "Size of basic graph"
with graph::basic by walker::tally {
    assert(visited.length == 5);
    assert(count > 5);
}

test "Size of a bit fancier graph"
with graph {
    has anchor root;
    spawn {
        root = spawn node::generic;
        spawn root --> graph::basic; spawn root --> graph::basic;
    }
} by walker::tally {
    assert(visited.length == 11);
    assert(count > 11);
}