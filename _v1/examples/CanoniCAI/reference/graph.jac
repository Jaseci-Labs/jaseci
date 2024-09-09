import {*} with "./dialogue.jac";
import {*} with "./faq.jac";

graph tesla_ai {
    has anchor dialogue_root;
    spawn {
        dialogue_root = spawn node::dialogue_root;
        test_drive_state = spawn node::test_drive_state;
        td_confirmation = spawn node::td_confirmation;
        td_confirmed = spawn node::td_confirmed;
        td_canceled = spawn node::td_canceled;

        faq_root_state = spawn node::faq_root;

        dialogue_root +[intent_transition(intent="test drive")]+> test_drive_state;
        dialogue_root +[intent_transition(intent="i have a question")]+> faq_root_state;

        test_drive_state +[entity_transition(entities=["name", "address"])]+> td_confirmation;
        test_drive_state +[intent_transition(intent="provide name or address")]+> test_drive_state;
        test_drive_state +[intent_transition(intent="cancel")]+> td_canceled;

        td_confirmation +[intent_transition(intent="yes")]+> td_confirmed;
        td_confirmation +[intent_transition(intent="no")]+> test_drive_state;
        td_confirmation +[intent_transition(intent="cancel")]+> td_canceled;
    }
}
