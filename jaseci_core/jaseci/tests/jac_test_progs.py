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


check_type_built_in = """
walker init {
    with entry {
        _d = {
            "key1": 0,
            "key2": 2,
            "key3": 3,
            "key4": 4,
            "key5": 5
        };

        report _d.key1 == 0;

        _dd = {
            "keys": _d,
            "key6": 6,
            "key7": 7,
            "key8": 8,
            "key9": 9
        };

        _d1 = {};
        _d2 = {};

        _d1 = _dd.dict::copy;
        _d2 = _dd.copy();

        _d["key1"] = 1;

        // save 1 since we used copy
        report _d1["keys"]["key1"] == 1;
        report _d2["keys"]["key1"] == 1;

        _d1.dict::clear;
        _d2.clear();

        report _d1 == {};
        report _d2 == {};

        _d1 = _dd.dict::deepcopy;
        _d2 = _dd.deepcopy();

        _d["key1"] = 0;

        // still 1 since we used deepcopy
        report _d1["keys"]["key1"] == 1;
        report _d2["keys"]["key1"] == 1;

        report _d1.items() == [
            [ "keys", { "key1": 1, "key2": 2, "key3": 3, "key4": 4, "key5": 5 } ],
            [ "key6", 6 ],
            [ "key7", 7 ],
            [ "key8", 8 ],
            [ "key9", 9 ]
        ];

        report _d1.dict::items == _d2.items();

        report _d1.keys == [ "keys", "key6", "key7", "key8", "key9" ];
        report _d1.dict::keys == _d2.keys;

        report _d1.values() == [ { "key1": 1, "key2": 2, "key3": 3, "key4": 4, "key5": 5 }, 6, 7, 8, 9 ];
        report _d1.dict::values == _d2.values();

        _d1.dict::update({"key10": 10});
        _d2.update({"key10": 10});

        report _d1.dict::get("key10") == _d2.get("key10");

        report _d1.dict::pop("key9") == _d2.pop("key9");

        report _d1.dict::popitem == _d2.popitem();

        report _d1.dict::get("key10", 11) == _d2.get("key10", 11);

        # -------------------- STRING -------------------- #

        _s1 = "aA bB";
        _s2 = "aA bB";

        report _s1.title() == "Aa Bb";
        report _s1.str::title == _s2.title();

        report _s1.capitalize() == "Aa bb";
        report _s1.str::capitalize == _s2.capitalize();

        _s1 = "AabB";
        _s2 = "AabB";

        report _s1.swap_case() == "aABb";
        report _s1.str::swap_case == _s2.swap_case();

        _s1 = "Abc123";
        _s2 = "Abc123";

        report _s1.is_alnum();
        report _s1.str::is_alnum == _s2.is_alnum();

        _s1 = "abc";
        _s2 = "abc";

        report _s1.upper() == "ABC";
        report _s1.str::upper == _s2.upper();

        report _s1.is_alpha();
        report _s1.str::is_alpha == _s2.is_alpha();

        report _s1.is_lower();
        report _s1.str::is_lower == _s2.is_lower();

        _s1 = "123";
        _s2 = "123";

        report _s1.is_digit();
        report _s1.str::is_digit == _s2.is_digit();

        _s1 = "My Title";
        _s2 = "My Title";

        report _s1.is_title();
        report _s1.str::is_title == _s2.is_title();

        _s1 = "ABC";
        _s2 = "ABC";

        report _s1.is_upper();
        report _s1.str::is_upper == _s2.is_upper();

        report _s1.lower() == "abc";
        report _s1.str::lower == _s2.lower();

        _s1 = " \\n\\t\\r";
        _s2 = " \\n\\t\\r";

        report _s1.is_space();
        report _s1.str::is_space == _s2.is_space();

        _s1 = "{\\\"test\\\":1}";
        _s2 = "{\\\"test\\\":1}";

        report _s1.load_json() == {"test":1};
        report _s1.str::load_json == _s2.load_json();

        _s1 = "A B";
        _s2 = "A B";

        report _s1.split(" ") == ["A", "B"];
        report _s1.str::split(" ") == _s2.split(" ");

        _s1 = "    A    ";
        _s2 = "    A    ";

        report _s1.strip() == "A";
        report _s1.str::strip == _s2.strip();

        report _s1.lstrip() == "A    ";
        report _s1.str::lstrip == _s2.lstrip();

        report _s1.rstrip() == "    A";
        report _s1.str::rstrip == _s2.rstrip();

        _s1 = "abcdea";
        _s2 = "abcdea";

        report _s1.count("a") == 2;
        report _s1.str::count("a") == _s2.count("a");

        report _s1.find("c") == 2;
        report _s1.str::find("c") == _s2.find("c");

        _s1 = "a b c";
        _s2 = "a b c";

        report _s1.split(" ") == ["a","b","c"];
        report _s1.str::split == _s2.split();

        _s1 = " ";
        _s2 = " ";

        report _s1.join(["a","b","c"]) == "a b c";
        report _s1.str::join(["a","b","c"]) == _s2.join(["a","b","c"]);

        report _s1.join("a","b","c") == "a b c";
        report _s1.str::join("a","b","c") == _s2.join("a","b","c");

        _s1 = "abcde";
        _s2 = "abcde";

        report _s1.startswith("abc");
        report _s1.str::startswith("abc") == _s2.startswith("abc");

        report _s1.endswith("cde");
        report _s1.str::endswith("cde") == _s2.endswith("cde");

        report _s1.replace("c", "f") == "abfde";
        report _s1.str::replace("c", "f") == _s2.replace("c", "f");

        _s1 = "aaabcdeaaa";
        _s2 = "aaabcdeaaa";

        report _s1.strip("a") == "bcde";
        report _s1.str::strip("a") == _s2.strip("a");

        report _s1.lstrip("a") == "bcdeaaa";
        report _s1.str::lstrip("a") == _s2.lstrip("a");

        report _s1.rstrip("a") == "aaabcde";
        report _s1.str::rstrip("a") == _s2.rstrip("a");

        # -------------------- LIST -------------------- #

        _l = [5,1,3,2];

        _ll = [1,0,2,9,3,_l,8,4,7,5,6];

        report _ll.length == 11;

        _l1 = _ll.list::copy;
        _l2 = _ll.copy();

        _l[0] = 4;

        report _l1[5][0] == 4;
        report _l2[5][0] == 4;

        _l1.clear();
        _l2.list::clear;

        report _l1 == [];
        report _l1 == _l2;

        _l1 = _ll.list::deepcopy;
        _l2 = _ll.deepcopy();

        _l[0] = 5;

        report _l1[5][0] == 4;
        report _l2[5][0] == 4;

        _l1.reverse();
        report _l1 == [6, 5, 7, 4, 8, [4,1,3,2], 3, 9, 2, 0, 1];

        _l2.list::reverse;
        report _l1 == _l2;

        report _l1.reversed() == [1,0,2,9,3,[4,1,3,2], 8,4,7,5,6];
        report _l1.list::reversed == _l2.reversed();

        _l1 = [6, 5, 7, 4, 8, 3, 9, 2, 0, 1];
        _l2 = [6, 5, 7, 4, 8, 3, 9, 2, 0, 1];

        _l1.sort();
        _l2.list::sort;

        report _l1 == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9];
        report _l1 == _l2;

        report _l1.max() == 9;
        report _l1.list::max == _l2.max();

        report _l1.min() == 0;
        report _l1.list::min == _l2.min();

        report _l1.idx_of_max() == 9;
        report _l1.list::idx_of_max == _l2.idx_of_max();

        report _l1.idx_of_min() == 0;
        report _l1.list::idx_of_min == _l2.idx_of_min();

        report _l1.pop() == _l2.list::pop;

        _l1.append(9);
        _l2.list::append(9);

        _l1.extend([10,11]);
        _l2.list::extend([10,11]);

        _l1.insert(0, -1);
        _l2.list::insert(0, -1);

        _l1.remove(-1);
        _l2.list::remove(-1);

        report _l1.index(10) == 10;
        report _l1.list::index(11) == _l2.index(11);

        _l1.append(10);
        _l2.list::append(10);

        _l1.append(10);
        _l2.list::append(10);

        report _l1.count(10) == 3;
        report _l1.list::count(10) == _l2.count(10);

        _l1 = _l1.pop(13);

        report _l1 == _l2.list::pop(13);
    }
}
"""
