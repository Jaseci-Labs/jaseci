import {graph::dummy, node::{banana, apple, testnode}} with "./jac_tests.jac";
# import {*} with "./jac_tests.jac";
# import {graph::dummy, node*} with "./jac_tests.jac";

walker init {
    has num=4;
    with entry {
        spawn here --> graph::dummy;
    }
    report here.context;
    report num;
    take -->;
}