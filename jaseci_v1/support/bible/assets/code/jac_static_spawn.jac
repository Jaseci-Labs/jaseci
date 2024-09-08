graph hlp_graph {
    has anchor graph_root;
    spawn {
        graph_root = spawn node::state(name="root_state");
        user_node = spawn node::user;

        state_home_price_inquiry = spawn node::state(name="home_price_inquiry");
        state_prob_of_approval = spawn node::state(name="prob_of_approval");

        graph_root -[user]-> user_node;

        graph_root -[transition(intent_label = "home price inquiry")]-> state_home_price_inquiry;
        graph_root -[transition(intent_label = "robability of loan approval")]-> state_prob_of_approval;
        state_home_price_inquiry -[transition(intent_label = "specifying location")]-> state_home_price_inquiry;
        state_home_price_inquiry -[transition(intent_label = "home price inquiry")]-> state_home_price_inquiry;

        state_home_price_inquiry -[transition(intent_label = "probability of loan approval")]-> state_prob_of_approval;
        state_prob_of_approval -[transition(intent_label = "home price inquiry")]-> state_home_price_inquiry;
    }
}