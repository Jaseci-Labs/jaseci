bug_check1 = \
    """
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


action_load_std_lib = \
    """
    walker aload {
        report std.actload_local('jaseci/tests/infer.py');
    }
    """


globals = \
    """
    global a = "testing";

    walker init {
        report global.a;
        global.a = 56;
        report global.a;
    }
    """

net_root_std_lib = \
    """
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


or_stmt = \
    """
    walker init {
        x = 3.4;
        y = "Hello";
        if(x == 3.45 or y == "Hello"):
            report [x, y];
    }
    """

nd_equals_error_correct_line = \
    """
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
