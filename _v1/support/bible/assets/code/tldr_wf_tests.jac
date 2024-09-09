import {*} with "./cai.jac";

walker get_states {
    has anchor path = [];
    take -->;
}

test "Travesal touches all nodes"
with graph::basic_gph by walker::get_states {
    std.out(path.length);
    assert(path.length==7);
}