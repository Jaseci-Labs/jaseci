import {edge::{trans_ner, trans_intent, trans_qa}} with "./edges.jac";
import {node::{state, hop_state}} with "./nodes.jac";

graph basic_gph {
    has anchor conv_root;
    spawn {
        conv_root = spawn node::state(name="Conv Root");

        appt = spawn conv_root -[trans_intent(intent="appointment")]->
            node::hop_state(name="Appointments");

        spawn appt -[trans_intent(intent="create")]->
            node::state(name="Create an appoitnment");
        spawn appt -[trans_intent(intent="cancel")]->
            node::state(name="Cancel an appoitnment");
        spawn appt -[trans_intent(intent="reschedule")]->
            node::state(name="Reschedule an appoitnment");

        service = spawn conv_root -[trans_intent(intent="service info")]->
            node::hop_state(name="Services");

        spawn service -[trans_intent(intent="manicures")]->
            node::state(name="About manicures");
        spawn service -[trans_intent(intent="haircuts")]->
            node::state(name="About haircuts");
        spawn service -[trans_intent(intent="makeup")]->
            node::state(name="About makeup");
    }

}