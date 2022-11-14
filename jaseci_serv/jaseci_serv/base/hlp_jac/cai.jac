import {
    node::{state, faq_state, faq_answer_state}
} with "./nodes.jac";

import {
    edge::{transition, user_link}
} with "./edges.jac";

import {
    node::{user, user_dir}
} with "./user.jac";

import {*} with "./globals.jac";

walker talker {
    has question, user_id="example", start_new_dialogue = false, overwrite_intent = "", overwrite_entity = {};
    has hoping = true; # If the walker needs to make the transition
    has starting_state;
    has predicted_intent = "";
    has intent_confidence = 0;
    has extracted_entities = {};
    has user_context = {};
    has dialogue_context = {};
    has answer;
    has state_for_continuing;
    has destination_state;
    has resp_payload = {};

    root {
        take --> node::cai_root;
    }
    cai_root {
        take --> node::user_dir;
    }
    user_dir {
        take -[user_link(user_id==user_id)]-> node::user;
    }
    user {
        # std.log("starting_state");
        # std.log(starting_state.name);
        starting_state = here.last_conv_state;
        dialogue_context = here.dialogue_context;

        take starting_state;
    }
    state, faq_state {
        if (hoping) {
            # By default, the walker only takes one hop
            // # This can be overwritten in nodes abilities to sk the
            # walker to extra hop(s) if needed
            # e.g. for FAQ route, we take 2 hops instead of 1
            hoping = false;
            std.log("traverling to ");
            std.log(destination_state.name);
            take destination_state else {
                report {
                    "name": "out_of_scope",
                    "response": "Sorry, I can't handle that just yet.",
                    "state": {},
                    "payload": resp_payload
                };
            }
        }
   }
}

walker ask {
    has question;
    spawn *(global.faq_state) walker::talker(question=question);
}

walker read {
    has source_url;
    has source_text;
    root: take --> node::cai_root;
    cai_root: take --> node::state(name=="conv_root_state");
    state: take --> node::faq_state;
}

walker forget {
    root: take --> node::cai_root;
    cai_root: take --> node::state(name=="conv_root_state");
    state: take --> node::faq_state;
}

walker maintainer {
    has user_id, user_context, dialogue_context, last_conv_state;
    root: take --> node::cai_root;
    cai_root: take --> node::user_dir;
    user_dir: take -[user_link(user_id==user_id)]-> node::user;
}
