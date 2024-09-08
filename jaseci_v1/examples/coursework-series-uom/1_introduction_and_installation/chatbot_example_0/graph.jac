// Defining the nodes
node faq_root;
node faq_state {
    has question;
    has answer;
}


// Static graph definition
graph faq {
    has anchor faq_root;
    spawn {

        faq_root = spawn node::faq_root;

    }
}
