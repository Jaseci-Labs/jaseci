import {*} with "./dialogue.jac";

graph bot_root {
    has anchor dialogue_root;
    spawn {
        dialogue_root = spawn node::dialogue_root;
        joke_state = spawn node::joke_state;
        ask = spawn node::ask;
        affirm = spawn node::affirm;
        deny = spawn node::deny;
        happy = spawn node::happy;

        faq_root = spawn graph::faq;

        dialogue_root +[intent_transition(intent="greet")]+> joke_state;
        dialogue_root +[intent_transition(intent="faq")]+> faq_root;
        dialogue_root +[intent_transition(intent="happy")]+> happy; 
        dialogue_root +[intent_transition(intent="affirm")]+> affirm;
        dialogue_root +[intent_transition(intent="deny")]+> deny;


        joke_state +[entity_transition(entities=["name"])]+> ask;
        joke_state +[intent_transition(intent="deny")]+> deny;
 

        ask +[intent_transition(intent="affirm")]+> affirm;
        ask +[intent_transition(intent="deny")]+> deny;
    }
}
