spawn_graph_node = """
    node test_node {has name;}
    graph test_graph {
        has anchor graph_root;
        spawn {
            graph_root =
                spawn node::test_node(name="graph_root_node_name");
        }
    }
    walker init {
        root {
            spawn here ++> graph::test_graph;
            take --> node::test_node;
        }
        test_node {
            std.out(here.name);
        }
    }
    """

basic_arith = """
    walker init {
        a = 4 + 4;
        b = 4 * -5;
        c = 4 / 4;  # Returns a floating point number
        d = 4 - 6;
        e = a + b + c + d;
        std.out(a, b, c, d, e);
    }
    """

more_arith = """
    walker init {
        a = 4 ^ 4; b = 9 % 5; std.out(a, b);
    }
    """

compare = """
    walker init {
        a = 5; b = 6;
        std.out(a == b,
                a != b,
                a < b,
                a > b,
                a <= b,
                a >= b,
                a == b-1);
    }
    """

logical = """
    walker init {
        a = true; b = false;
        std.out(a,
                !a,
                a && b,
                a || b,
                a and b,
                a or b,
                !a or b,
                !(a and b));
    }
    """

assignments = """
    walker init {
        a = 4 + 4; std.out(a);
        a += 4 + 4; std.out(a);
        a -= 4 * -5; std.out(a);
        a *= 4 / 4; std.out(a);
        a /= 4 - 6; std.out(a);

        # a := here; std.out(a);
        # Noting existence of copy assign, described later
    }
    """

if_stmt = """
    walker init {
        a = 4; b = 5;
        if(a < b): std.out("Hello!");
    }
    """

else_stmt = """
    walker init {
        a = 4; b = 5;
        if(a == b): std.out("A equals B");
        else: std.out("A is not equal to B");
    }
    """

elif_stmt = """
    walker init {
        a = 4; b = 5;
        if(a == b): std.out("A equals B");
        elif(a > b): std.out("A is greater than B");
        elif(a == b - 1): std.out("A is one less than B");
        elif(a == b - 2): std.out("A is two less than B");
        else: std.out("A is something else");
    }
    """

for_stmt = """
    walker init {
        for i=0 to i<10 by i+=1:
            std.out("Hello", i, "times!");
    }
    """
while_stmt = """
    walker init {
        i = 5;
        while(i>0) {
            std.out("Hello", i, "times!");
            i -= 1;
        }
    }
    """

break_stmt = """
    walker init {
        for i=0 to i<10 by i+=1 {
            std.out("Hello", i, "times!");
            if(i == 6): break;
        }
    }
    """

continue_stmt = """
    walker init {
        i = 5;
        while(i>0) {
            if(i == 3){
                i -= 1; continue;
            }
            std.out("Hello", i, "times!");
            i -= 1;
        }
    }
    """

continue_stmt2 = """
    walker init {
        z=10;

        while(z>=0){
            z-=1;
            if(z<5){
                continue;
            }
            std.out("hello", z);
        }
    }
    """

destroy_disconn = """
    node testnode {
        has apple;
    }

    walker init{
        node1 = spawn here ++> node::testnode ;
        node2 = spawn here ++> node::testnode ;
        node1 ++> node2;
        std.out(-->);
        destroy node1;
        # All node destroys queue'd after walk
        # may not be a good idea, must think about it
        std.out(-->);
        here !--> node2;
        std.out('1', -->);
    }
    """

array_assign = """
    node testnode {
        has apple;
    }

    walker init{
        root {
            node1 = spawn here ++> node::testnode ;
            node1.apple = [[1,2],[3,4]];
            take node1;
        }
        testnode {
            a = [[0,0],[0,0]];
            std.out(a);
            a[0] = [1,1];
            std.out(a);
            std.out(here.apple);
            here.apple[1] = here.apple[0];
            std.out(here.apple);
        }
    }
    """

array_md_assign = """
    node testnode {
        has apple;
    }

    walker init{
        root {
            node1 = spawn here ++> node::testnode ;
            node1.apple = [[1,2],[3,4]];
            take node1;
        }
        testnode {
            std.out(here.apple);
            here.apple[0][1] = here.apple[0][0];
            std.out(here.apple);
        }
    }
    """

dereference = """
    node testnode {
        has apple;
    }

    walker init{
        root {
            node1 = spawn here ++> node::testnode ;
            std.out(&node1);
        }
    }
    """

pre_post_walking = """
    node testnode {
        has apple;
    }

    walker init {
        has count;

        with entry {
            count = 5;
            spawn here ++> node::testnode ;
            spawn here ++> node::testnode ;
            spawn here ++> node::testnode ;
            take -->;
        }

        testnode {
            count += 1;
        }

        with exit {std.out("count:",count);}
    }
    """

pre_post_walking_dis = """
    node testnode {
        has apple;
    }

    walker init {
        has count;

        with entry {
            count = 5;
            spawn here ++> node::testnode ;
            spawn here ++> node::testnode ;
            spawn here ++> node::testnode ;
            take -->;
        }

        testnode {
            count += 1;
            disengage;
            std.out("test");
        }

        with exit {std.out("count:",count);}
    }
    """

length = """
    node testnode {
        has apple;
    }

    walker init {
        spawn here ++> node::testnode ;
        spawn here ++> node::testnode ;
        spawn here ++> node::testnode ;
        std.out((-->).length);
        var = -->;
        std.out(var.length);
    }
    """

sort_by_col = """
    walker init {
        lst=[['b', 333],['c',245],['a', 56]];
        std.out(lst);
        std.out(std.sort_by_col(lst, 0));
        std.out(std.sort_by_col(lst, 0, true));
        std.out(std.sort_by_col(lst, 1));
        std.out(std.sort_by_col(lst, 1, true));
    }
    """

list_remove = """
    node testnode { has lst; }

    walker init {
        nd=spawn here ++> node::testnode ;
        nd.lst=[['b', 333],['c',245],['a', 56]];
        std.out(nd.lst);
        destroy nd.lst[1];
        std.out(nd.lst);
        destroy nd.lst[1];
        std.out(nd.lst);
    }
    """

can_action = """
    node testnode {
        has anchor A;
        can ptest {
            b=7;
            std.out(A,b);
            ::ppp;
        }
        can ppp {
            b=8;
            std.out(A,b);
        }
    }

    walker init {
        a= spawn here ++> node::testnode (A=56);
        a::ptest;
    }
    """

can_action_params = """
    node testnode {
        has anchor A;
        can ptest {
            b=7;
            std.out(A,b);
            ::ppp;
        }
        can ppp {
            b=8;
            std.out(A,b);
        }
    }

    walker init {
        a= spawn here ++> node::testnode (A=56);
        a::ptest(A=43);
        a::ptest(A=a.A+5);
    }
    """

cross_scope_report = """
    node testnode {
        has anchor A;
        can ptest {
            b=7;
            std.out(A,b);
            report A;
            ::ppp;
            skip;
            std.out("shouldnt show this");
        }
        can ppp {
            b=8;
            std.out(A,b);
            report b;
        }
    }

    walker init {
        a= spawn here ++> node::testnode (A=56);
        a::ptest;
        report here;
    }
    """

has_private = """
    node testnode {
        has apple;
        has private banana, grape;
    }

    walker init {
        root {
            spawn here ++> node::testnode (apple=5, banana=6, grape=1);
            take -->;
        }
        testnode {
            here.apple+=here.banana+here.grape;
            report here;
        }
    }
    """

array_idx_of_expr = """
    node testnode {
        has apple;
    }

    walker init {
        spawn here ++> node::testnode ;
        spawn here ++> node::testnode ;
        spawn here ++> node::testnode ;
        std.out((-->).length);
        var = -->[0];
        std.out([var].length);
    }
    """

dict_assign = """
    node testnode {
        has apple;
    }

    walker init{
        root {
            node1 = spawn here ++> node::testnode ;
            node1.apple = {"one": 1, "two": 2};
            take node1;
        }
        testnode {
            a =  {"three": 3, "four": 4};
            std.out(a);
            a["four"] = 55;
            std.out(a);
            std.out(here.apple);
            here.apple["one"] = here.apple["two"];
            std.out(here.apple["one"]);
        }
    }
    """

dict_md_assign = """
    node testnode {
        has apple;
    }

    walker init{
        root {
            node1 = spawn here ++> node::testnode ;
            node1.apple = {"one": {"inner": 44}, "two": 2};
            take node1;
        }
        testnode {
            std.out(here.apple);
            here.apple["one"]["inner"] = here.apple["two"];
            std.out(here.apple["one"]);
            std.out(here.apple["one"]['inner']);
        }
    }
    """

dict_keys = """
    node testnode {
        has apple;
    }

    walker init{
        root {
            node1 = spawn here ++> node::testnode ;
            node1.apple = {"one": {"inner": 44}, "two": 2};
            take node1;
        }
        testnode {
            std.out(here.apple);
            for i in here.apple.keys:
                if(i == 'one'):
                    for j in here.apple.keys:
                        if(j == 'two'):
                            here.apple[i]["inner"] = here.apple[j];
            std.out(here.apple["one"]);
            std.out(here.apple["one"]['inner']);
        }
    }
    """
cond_dict_keys = """
    node testnode {
        has apple;
    }

    walker init{
        root {
            node1 = spawn here ++> node::testnode ;
            node1.apple = {"one": {"inner": 44}, "two": 2};
            take node1;
        }
        testnode {
            std.out(here.apple);
            if('one' in here.apple.keys) {std.out('is here');}
            if('three' not in here.apple.keys) {std.out('also not here'); }
            if('three' in here.apple.keys) {std.out('SHOULD NOT PRINT'); }
        }
    }
    """

soft_max = """
    walker init{
        can vector.softmax;
        scores = [3.0, 1.0, 0.2];
        a=vector.softmax(scores);
        report a;
        std.out(a);
    }
    """

fam_example = """
    node man;
    node woman;

    edge mom;
    edge dad;
    edge married;

    walker create_fam {
        root {
            spawn here ++> node::man;
            spawn here ++> node::woman;
            --> node::man <+[married]+> --> node::woman;
            take -->;
        }
        woman {
            son = spawn here <+[mom]+ node::man;
            son <+[dad]+ <-[married]->;
        }
        man {
            std.out("I didn't do any of the hard work.");
        }
    }
    """

visitor_preset = """
    node person {
        has name;
        has byear;
        can date.quantize_to_year::std.time_now()::>byear with setter entry;
        can std.out::byear," from ",visitor.info:: with exit;
        can std.out::byear," init only from ",visitor.info:: with init exit;
    }

    walker init {
        has year=std.time_now();
        root {
            person1 = spawn here ++>
                node::person(name="Josh", byear="1995-01-01");
            take --> ;
        }
        person {
            spawn here walker::setter;
        }
    }

    walker setter {
        has year=std.time_now();
    }
    """

visitor_local_aciton = """
    node person {
        has name;
        has byear;
        can set_year with setter entry {
            byear = visitor.year;
        }
        can print_out with exit {
            std.out(byear, " from ", visitor.info);
        }
        can reset {  # <-- Could add 'with activity' for equivalent behavior
            byear = "1995-01-01";
            std.out("resetting year to 1995:", here.context);
        }
    }

    walker init {
        has year = std.time_now();
        has person1;
        root {
            person1 = spawn here ++> node::person;
            std.out(person1.context);
            person1::reset;
            take -->;
        }
        person {
            spawn here walker::setter;
            person1::reset(name="Joe");
        }
    }

    walker setter {
        has year = std.time_now();
    }
    """

copy_assign_to_edge = """
    node person: has name, age, birthday, profession;
    edge friend: has meeting_place;
    edge family: has kind;

    walker init {
        person1 = spawn here +[friend(meeting_place = "college")]+>
            node::person(name = "Josh", age = 32);
        person2 = spawn here +[family(kind = "sister")]+>
            node::person(name = "Jane", age = 30);

        twin1 = spawn here +[friend]+> node::person;
        twin2 = spawn here +[family]+> node::person;
        twin1 := person1;
        twin2 := person2;

        -->.edge[2] := -->.edge[0];
        -->.edge[3] := -->.edge[1];

        std.out("Context for our people nodes and edges:");
        for i in -->: std.out(i.context, '\\n', i.edge[0].context);
    }
    """
