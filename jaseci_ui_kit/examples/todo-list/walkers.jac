import {*} with "./nodes.jac";
edge tasks_task;
edge pages_page;

walker create_task {
    has name;

    root: take --> node::app;
    app: take --> node::tasks;

    tasks {
        task = spawn here -[tasks_task]-> node::task(name=name);

        report task;
        disengage;
    }
}

walker edit_task {
    has name;
    
    task {
        if(name): here.name = name;
        report here;
        disengage;
    }
}

walker delete_task {
    task {
        report here;
        destroy here;
        disengage;
    }
}

walker list_tasks {
    root: take --> node::app;
    app: take --> node::tasks;
    

    tasks {
        for task in -[tasks_task]-> {
            report task;
        }
        disengage;
    }
}

walker create_page {
    has anchor page;
    has name;
    has path;
    
    pages {
        page = spawn here -[pages_page]-> node::page(name=name, path=path);
        
        report page;
        disengage;
    }
}

walker register_page {
    // has payload={};
    has final;

    page {
        final = -->[0];
        take -->[0];
    }

    Component {
        if(here.loc==null): here.loc=payload;
        take -->;
    }

    with exit {
        report final.loc;
    }
}

walker list_pages {
    root: take --> node::app;
    app: take --> node::pages;
    

    pages {
        report here;
        for page in -[pages_page]-> {
            report page;
        }
        
        disengage;
    }
}
