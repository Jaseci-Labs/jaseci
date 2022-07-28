import {*} with "./nodes.jac";
import {*} with "./edges.jac";

walker talk {
    has question;
    has next_states = [];

    cai_state {

    }
}

graph tesla_sales_rep {
    has anchor state_test_drive;
    spawn {
        state_test_drive = spawn node::test_drive;
        state_collect_info  = spawn node::collect_info;
        state_confirmation = spawn node::confirmation;
        state_confirmed = spawn node::confirmed;
        state_canceled = spawn node::canceled;
    }
}