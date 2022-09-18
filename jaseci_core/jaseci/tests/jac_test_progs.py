bug_check1 = """
    node state {
        has cand_intents = [];
        # Collect possible intents from a given conversation state
        can collect_intents {
            for i in -[transition]->.edge {
                here.cand_intents += [i.intent_label];
            }
        }
    }
    edge transition {has intent_label;}
    walker test_walker {
        state {
            here::collect_intents;
        }
    }
    graph test_graph {
        has anchor state_node;
        spawn {
            state_node = spawn node::state;
            state_2 = spawn node::state;
            state_node -[transition(intent_label =
                        "THIS IS AN INTENT_LABEL")]-> state_2;
        }
    }

    walker init {
        spawn here --> graph::test_graph;
        spawn --> walker::test_walker;
        report -->[0].cand_intents;
        report -->;
    }

    test "Test"
    with graph::test_graph by walker::test_walker {
        assert(here.cand_intents == ['THIS IS AN INTENT_LABEL']);
    }
    """


action_load_std_lib = """
    walker aload {
        report std.actload_local('jaseci/tests/infer.py');
    }
    """


globals = """
    global a = "testing";

    walker init {
        report global.a;
        global.a = 56;
        report global.a;
    }
    """

net_root_std_lib = """
    walker init {
        root {
            report [here.info['jid'], net.root().info['jid']];
            spawn here --> node::generic;
            take -->;
        }
        generic {
            report [here.info['jid'], net.root().info['jid']];
        }
    }
    """


or_stmt = """
    walker init {
        x = 3.4;
        y = "Hello";
        if(x == 3.45 or y == "Hello"):
            report [x, y];
    }
    """

nd_equals_error_correct_line = """
    node plain{ has name="joe", noname;
    can stuff with entry {std.out(name + noname); }}

    walker init {
        root {
            spawn here --> node::plain;
            take -->;
        }
        plain {
            if(here.details['name'] == 'joe'):
                report here.info;
        }
    }
    """

strange_ability_bug = """
    node plain {
        can show with entry {
            report "Showing";
        }
    }

    walker init {
        root {
            spawn here --> node::plain;
        }
    }

    walker travel {
        take -->;
    }
    """

node_inheritance = """
    node plain {
        has a=5, b=7, c=7, d=8;
        can x with entry {
            report "plain.x";
        }
        can y {
            report "plain.y";
        }
    }

    node plain2 {
        has c=70, d=80;
        can x with entry {
            report "plain2.x";
        }
        can y {
            report "plain2.y";
        }
    }

    node super:plain:plain2 {
        has a=55, c=7;
        can x with entry {
            ::plain:x;
            report here.context;
            report "super.x";
        }
        can y {
            ::plain2:y;
            report "super.y";
        }
    }

    walker init {
        root {
            a=spawn here --> node::super;
        }
        take -->;
        super {
            here::y;
        }
    }
    """

inherited_ref = """
    node plain {
        has a=5, b=7, c=7, d=8;
        can x with entry {
            report "plain.x";
        }
        can y {
            report "plain.y";
        }
        can z with entry {
            report "Z triggered";
        }
    }

    node plain2:plain {
        has c=70, d=80;
        can x with entry {
            report "plain2.x";
        }
        can y {
            report "plain2.y";
        }
        can z with entry {
            report "New Z triggered";
        }
    }

    node super:plain2 {
        has a=55, c=7;
        can x with entry {
            ::plain:x;
            report here.context;
            report "super.x";
            ::z;
        }
        can y {
            ::plain2:y;
            report "super.y";
        }
    }

    walker init {
        root {
            spawn here --> node::super;
            spawn here --> node::plain;
            spawn here --> node::plain2;
        }
        take --> node::plain;
        plain {
            report here;
        }
    }
    """

node_inheritance_chain_check = """
    node plain {
        has a=5, b=7, c=7, d=8;
        can x with entry {
            report "plain.x";
        }
        can y {
            report "plain.y";
        }
    }

    node plain2 {
        has c=70, d=80;
        can x with entry {
            report "plain2.x";
        }
        can y {
            report "plain2.y";
        }
    }

    node super:plain {
        has a=55, c=7;
        can x with entry {
            ::plain:x;
            report here.context;
            report "super.x";
        }
        can y {
            ::plain2:y;
            report "super.y";
        }
    }

    walker init {
        root {
            a=spawn here --> node::super;
        }
        take -->;
        super {
            here::y;
        }
    }
    """

global_reregistering = """
    node plain;

    global a = '556';

    walker init {
        root {
            spawn here - -> node::plain;
            spawn here - -> node::plain;
            spawn here - -> node::plain;
        }
        report global.a;
        take - ->;
    }
    """

vector_cos_sim_check = """
    node plain;

    walker init {
        a=[1,2,3];
        b=[4,5,6];
        report vector.cosine_sim(a,b);
    }
    """

multi_breaks = """
    node plain {
        has anchor val=0;
        can breakdance {
            for i=0 to i<10 by i+=1 {
                for j=0 to j<20 by j+=1:
                    if(j==12) {
                        val+=j;
                        break;
                    }
                report "here";
                if(i==6){
                    val+=i;
                    break;
                }
            }
            break;
            val+=100;
        }
    }

    walker init {
        nd=spawn here --> node::plain;
        nd::breakdance;
        nd::breakdance;
        report nd.val;
    }
    """

reffy_deref_check = """
    node plain{has expected_answer;}

    walker init {
        nd = spawn here --> node::plain;
        spawn here --> node::plain;

        report *&-->[0] == *&-->[1];

        actual_answer = -->[1];
        nd.expected_answer = &-->[1];
        report *&actual_answer == *nd.expected_answer;
    }
    """

vanishing_can_check = """
    node plain {
        has name;
        can infer.year_from_date;
    }

    walker init {
        root {
            take --> node::plain else {
                nd=spawn here --> node::plain;
                report nd.info['jid'];
                disengage;
            }
        }
        plain {
            report infer.year_from_date("2022-05-05");
        }
    }
    """

jasecilib_alias_list = """
    walker init {
        report jaseci.alias_list();
    }
    """

jasecilib_params = """
    walker init {
        report jaseci.graph_list(true);
    }
    """

jasecilib_create_user = """
    walker init {
        report jaseci.master_create("daman@gmail.com");
    }
    """

root_is_node_type = """
    walker init {
        report here.type;
    }
    """

walker_with_exit_after_node = """
    node echeck {
        has a=3;
        can dostuff with exit {
            report a;
        }
    }

    walker init {
        has a=0;
        with entry {
            a+=1;
        }
        root {
            spawn here --> node::echeck;
            spawn here --> node::echeck;
            spawn here --> node::echeck;
            spawn here --> node::echeck;
        }
        take -->;
        report a;
        with exit {
            report 43;
        }
    }
    """


depth_first_take = """
    node a {
        has num;
    }

    walker init {
        root {
            n1=spawn node::a(num=1);
            n2=spawn node::a(num=2);
            n3=spawn node::a(num=3);
            n4=spawn node::a(num=4);
            n5=spawn node::a(num=5);
            n6=spawn node::a(num=6);
            n7=spawn node::a(num=7);

            here --> n1 --> n2 --> n3;
                            n2 --> n4;
                     n1 --> n5 --> n6;
                            n5 --> n7;
        }

        a: report here.num;
        take:dfs -->;
    }
    """

breadth_first_take = """
    node a {
        has num;
    }

    walker init {
        root {
            n1=spawn node::a(num=1);
            n2=spawn node::a(num=2);
            n3=spawn node::a(num=3);
            n4=spawn node::a(num=4);
            n5=spawn node::a(num=5);
            n6=spawn node::a(num=6);
            n7=spawn node::a(num=7);

            here --> n1 --> n2 --> n3;
                            n2 --> n4;
                     n1 --> n5 --> n6;
                            n5 --> n7;
        }

        a: report here.num;
        take:bfs -->;
    }
    """


inheritance_override_here_check = """
    node a {
        has x=5, y=3, z=1;
        can sum {
            z = x+y+z;
            report z;
        }
    }

    node b:a {
        can sum {
            z = x-y-z;
            report x-y;
        }
    }

    node c:a {
        can sum {
            ::a:sum;
            z=z+1;
            report here.z;
        }
    }

    walker init {
        n1 = spawn here --> node::a;
        n2 = spawn here --> node::c;
        -->[0]::sum;
        -->[1]::sum;
    }
    """

dot_private_hidden = """
    node a {
        has x="56";
        has private j="5566669";
    }

    walker init {
        n1 = spawn here --> node::a;
        n2 = spawn here --> node::a;
    }
    """

check_destroy_node_has_var = """
    node a {
        has x;
    }

    walker create {
        n = spawn here --> node::a;
        n.x = spawn node::a;
        report n.x.type;
    }

    walker remove {
        n=-->[0];
        destroy n.x;
        report n.x.type;
    }
"""

check_dict_for_in_loop = """
    walker for_loop_dict {
        with entry {
            testing = {
                "test1": 1,
                "test2": 2,
                "test3": 3
            };

            for key in testing {
                report key.str + " : " + testing[key].str;
            }

            for key, val in testing {
                report key.str + " : " + val.str;
            }

            testing = [5,6,7];

            for key in testing {
                report key;
            }

            for key, val in testing {
                report key.str + " : " + val.str;
            }
        }
    }

    walker var_as_key_for_dict {
        with entry {
            key = "key1";
            not_str_key = 1;
            testing = {
                key: key,
                "key2": 2,
                not_str_key: not_str_key
            };

            report testing;
        }
    }
"""

check_new_builtin = """
    walker init {
        with entry {
            a = {"test":"test"};

            // dict get with default if not existing
            b = a.dict::get("t", 1);

            // string join single param array
            c = " ".str::join([1,2,3,4]);

            // string join multiparams
            d = " ".str::join(1,2,3,4);
            report a;
            report b;
            report c;
            report d;
        }
    }
"""

continue_issue = """
    walker init {
        root {
            for i=0 to i<10 by i+=1 {
                if(i==9):
                    continue;
                if(i):
                    report i;
            }
            report "apple";
        }
    }
"""
