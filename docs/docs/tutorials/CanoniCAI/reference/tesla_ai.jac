import {*} with "./graph.jac";
import {*} with "./ai_model.jac";
import {*} with "./faq.jac";

walker talk {
    has question, interactive = false;
    has wlk_ctx = {
        "intent": null,
        "entities": {},
        "prev_state": null,
        "next_state": null,
        "respond": false,
        "in_faq": false
    };
    has response;
    root {
        take --> node::dialogue_root;
    }
    cai_state {
        if (!question && interactive) {
            question = std.input("Question (Ctrl-C to exit)> ");
            here::init_wlk_ctx;
        }
        here::nlu;
        here::process;
        if (visitor.wlk_ctx["respond"]) {
            here::nlg;
            if (interactive): std.out(response);
            else {
                yield report response;
                here::init_wlk_ctx;
            }
            question = null;
            take here;
        } else {
            take visitor.wlk_ctx["next_state"] else: take here;
        }
    }
}

walker init {
    std.actload_module("jac_nlp.use_qa");
    std.actload_module("jac_nlp.bi_enc");
    std.actload_module("jac_nlp.tfm_ner");
    root {
        dialogue_root = spawn here ++> graph::tesla_ai;
        spawn dialogue_root walker::ingest_faq(kb_file="tesla_faq.json");
    }
}
