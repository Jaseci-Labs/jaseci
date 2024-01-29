walker walker_1 {
    can create with `<root> entry;
}

node node_a {
    has val: int;

    can print_something with walker_1 entry;
}

walker walker_2 {
    can skip_root with `<root> entry {
        visit -->;
    }

    can do_something with node_a entry {}
}
#creating five nodes

:walker:walker_1:can:create {
    end = <here>;
    for i=0 to i<5 by i+=1  {
        end ++> (end := node_a(val=i + 1));
    }
    visit -->;
}

:node:node_a:can:print_something -> str {
    print(f"walker_1 entered to {<self>}");
    visit -->;
}

with entry {
    walker_1() spawn <root>; #walker_1 statrt walking from root node
    <root> spawn walker_2(); #after walker_1 finish walking walker_2 start walking to nodes
}
