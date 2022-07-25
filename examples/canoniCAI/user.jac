import {
    edge::{user_link}
} with "./edges.jac";
import {*} with "./cai.jac";
import {*} with "./globals.jac";

# User node
node user {
    has id;
    has profile = {};
    has dialogue_context = {};
    has last_conv_state = null;
    has load_from_api = "";

    can start_conv with talker entry {
        if (here.profile == {}) {
            ::init_user;
        }
        visitor.user_context = here.profile;
        if (here.last_conv_state == null) {
            here.last_conv_state = *(global.conv_root_state);
        }
        if(visitor.start_new_dialogue){
            here.dialogue_context = {};
            here.last_conv_state = *(global.conv_root_state);
        }

        visitor.starting_state = here.last_conv_state;
        visitor.dialogue_context = here.dialogue_context;
    }

    can update_with_conv with maintainer entry {
        here.profile.d::update(visitor.user_context);
        here.dialogue_context.d::update(visitor.dialogue_context);
        here.last_conv_state = visitor.last_conv_state;
    }

    can init_user with init entry {
        default_fields = {
            "personal_info": {},
            "db": {},
            "history": {}
        };
            
        if (here.id == "example") {
            here.profile = default_fields;
        }
        elif(here.load_from_api != ""){
            payload = file.load_json(here.load_from_api);
            here.profile = default_fields;
            here.profile["personal_info"] = payload["personal_info"];
        }
    }
}

# User directory node
node user_dir {
    can init_users with init entry {
        # Install an example user
        if(-[user_link(user_id=="example")]->.length == 0) {
            spawn here -[user_link(user_id="example")]-> node::user(id="example");
        }

        # Install all users from json
        users = file.load_json('data/users/user_dir.json');

        for u in users {
            spawn here -[user_link(user_id=u["user_id"])]-> node::user(id=u["user_id"], load_from_api=u["user_json"]);
        }
    }
}

walker update_user {
    root: take --> node::cai_root;
    cai_root: take --> node::user_dir;
    user_dir: take --> node::user;
}