import {*} with "./ancestry/main.jac";

walker run_chatbot {
    has query;
    intent  = spawn here walker::find_intent(query=query);
    if (intent == "get_parents") : spawn here walker::get_parents;
    if (intent == "get_siblings") : spawn here walker::get_siblings;
}

walker find_intent {
    can bi_enc.infer;
    has query;
    has anchor intent;
    intent = bi_enc.infer(contexts=[query], candidates=["get_parents", "get_siblings"]);
    report intent;
}

walker get_parents {
    has name;
    has child_id;
    root: take-->node::family_root;
    family_root{
        name = std.input("What is the name of the person you want to know about? ");
        take-->node::person;
    }
    person {
        if (!name): name = here.name;
        if (here.name == name) {
            child_id = here.id;
            take<--node::person;
        }
        if (child_id and child_id in here.children) {
            report here.name;
            disengage;
        }
    }
}

walker get_siblings {
    has name;
    has child_id;
    root: take-->node::family_root;
    family_root{
        name = std.input("What is the name of the person you want to know about? ");
        take-->node::person;
    }
    person {
        if (!name): name = here.name;
        if (here.name == name) {
            child_id = here.id;
            take<--node::person;
        }
        if (child_id and child_id in here.children) {
            for sibling in <-[child]-node::person {
                if (sibling.id != child_id): report sibling.name;
            }
            disengage;
        }
    }
}