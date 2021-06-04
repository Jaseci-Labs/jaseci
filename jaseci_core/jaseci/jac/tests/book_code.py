basic_arith = \
    """
    walker init {
        a = 4 + 4;
        b = 4 * -5;
        c = 4 / 4;  # Returns a floating point number
        d = 4 - 6;
        e = a + b + c + d;
        std.out(a, b, c, d, e);
    }
    """

more_arith = \
    """
    walker init {
        a = 4 ^ 4; b = 9 % 5; std.out(a, b);
    }
    """

compare = \
    """
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

logical = \
    """
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

assignments = \
    """
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

if_stmt = \
    """
    walker init {
        a = 4; b = 5;
        if(a < b): std.out("Hello!");
    }
    """

else_stmt = \
    """
    walker init {
        a = 4; b = 5;
        if(a == b): std.out("A equals B");
        else: std.out("A is not equal to B");
    }
    """

elif_stmt = \
    """
    walker init {
        a = 4; b = 5;
        if(a == b): std.out("A equals B");
        elif(a > b): std.out("A is greater than B");
        elif(a == b - 1): std.out("A is one less than B");
        elif(a == b - 2): std.out("A is two less than B");
        else: std.out("A is something else");
    }
    """

for_stmt = \
    """
    walker init {
        for i=0 to i<10 by i+=1:
            std.out("Hello", i, "times!");
    }
    """
while_stmt = \
    """
    walker init {
        i = 5;
        while(i>0) {
            std.out("Hello", i, "times!");
            i -= 1;
        }
    }
    """

break_stmt = \
    """
    walker init {
        for i=0 to i<10 by i+=1 {
            std.out("Hello", i, "times!");
            if(i == 6): break;
        }
    }
    """

continue_stmt = \
    """
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

destroy_disconn = \
    """
    node test {
        has apple;
    }

    walker init{
        node1 = spawn here --> node::test;
        node2 = spawn here --> node::test;
        node1 --> node2;
        std.out(-->);
        destroy node1;
        std.out(-->);
        here !--> node2;
        std.out('1', -->);
    }
    """

array_assign = \
    """
    node test {
        has apple;
    }

    walker init{
        root {
            node1 = spawn here --> node::test;
            node1.apple = [[1,2],[3,4]];
            take node1;
        }
        test {
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

array_md_assign = \
    """
    node test {
        has apple;
    }

    walker init{
        root {
            node1 = spawn here --> node::test;
            node1.apple = [[1,2],[3,4]];
            take node1;
        }
        test {
            std.out(here.apple);
            here.apple[0][1] = here.apple[0][0];
            std.out(here.apple);
        }
    }
    """

dereference = \
    """
    node test {
        has apple;
    }

    walker init{
        root {
            node1 = spawn here --> node::test;
            std.out(&node1);
        }
    }
    """

pre_post_walking = \
    """
    node test {
        has apple;
    }

    walker init {
        has count;

        with entry {
            count = 5;
            spawn here --> node::test;
            spawn here --> node::test;
            spawn here --> node::test;
            take -->;
        }

        test {
            count += 1;
        }

        with exit {std.out("count:",count);}
    }
    """

pre_post_walking_dis = \
    """
    node test {
        has apple;
    }

    walker init {
        has count;

        with entry {
            count = 5;
            spawn here --> node::test;
            spawn here --> node::test;
            spawn here --> node::test;
            take -->;
        }

        test {
            count += 1;
            disengage;
            std.out("test");
        }

        with exit {std.out("count:",count);}
    }
    """

length = \
    """
    node test {
        has apple;
    }

    walker init {
        spawn here --> node::test;
        spawn here --> node::test;
        spawn here --> node::test;
        std.out((-->).length);
        var = -->;
        std.out(var.length);
    }
    """

sort_by_col = \
    """
    walker init {
        lst=[['b', 333],['c',245],['a', 56]];
        std.out(lst);
        std.out(std.sort_by_col(lst, 0));
        std.out(std.sort_by_col(lst, 0, 'reverse'));
        std.out(std.sort_by_col(lst, 1));
        std.out(std.sort_by_col(lst, 1, 'reverse'));
    }
    """

list_remove = \
    """
    node test { has lst; }

    walker init {
        nd=spawn here --> node::test;
        nd.lst=[['b', 333],['c',245],['a', 56]];
        std.out(nd.lst);
        nd.lst.destroy(1);
        std.out(nd.lst);
        std.out(nd.lst.destroy(1));
    }
    """

can_action = \
    """
    node test {
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
        a= spawn here --> node::test(A=56);
        a::ptest;
    }
    """

cross_scope_report = \
    """
    node test {
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
        a= spawn here --> node::test(A=56);
        a::ptest;
        report here;
    }
    """

has_private = \
    """
    node test {
        has apple;
        has private banana, grape;
    }

    walker init {
        root {
            spawn here --> node::test(apple=5, banana=6, grape=1);
            take -->;
        }
        test {
            here.apple+=here.banana+here.grape;
            report here;
        }
    }
    """

array_idx_of_expr = \
    """
    node test {
        has apple;
    }

    walker init {
        spawn here --> node::test;
        spawn here --> node::test;
        spawn here --> node::test;
        std.out((-->).length);
        var = -->[0];
        std.out([var].length);
    }
    """

dict_assign = \
    """
    node test {
        has apple;
    }

    walker init{
        root {
            node1 = spawn here --> node::test;
            node1.apple = {"one": 1, "two": 2};
            take node1;
        }
        test {
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

dict_md_assign = \
    """
    node test {
        has apple;
    }

    walker init{
        root {
            node1 = spawn here --> node::test;
            node1.apple = {"one": {"inner": 44}, "two": 2};
            take node1;
        }
        test {
            std.out(here.apple);
            here.apple["one"]["inner"] = here.apple["two"];
            std.out(here.apple["one"]);
            std.out(here.apple["one"]['inner']);
        }
    }
    """

dict_keys = \
    """
    node test {
        has apple;
    }

    walker init{
        root {
            node1 = spawn here --> node::test;
            node1.apple = {"one": {"inner": 44}, "two": 2};
            take node1;
        }
        test {
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

soft_max = \
    """
    walker init{
        can vector.softmax;
        scores = [3.0, 1.0, 0.2];
        a=vector.softmax(scores);
        report a;
        std.out(a);
    }
    """
