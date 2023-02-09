import {*} with "./graph.jac";

walker talk {
    has question;
    has wlk_ctx = {};
    has response;
    root {
        take --> node::dialogue_root;
    }
    cai_state {
        if (!question) {
            question = std.input("JTalk (Ctrl-C to exit)> ");
            here::init_wlk_ctx;
        }
        here::nlu;
        here::process;
        if (visitor.wlk_ctx["respond"]) {
            here::nlg;
            std.out(response);
            question = null;
            take here;
        } else {
            take visitor.wlk_ctx["next_state"] else: take here;
        }
    }
}

walker init {
    root {
        spawn here ++> graph::bot_root;
        spawn here walker::talk;
    }
}
