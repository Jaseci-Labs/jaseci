

walker get_props {
    has anchor props = {};

    for prop in here.context.dict::keys {
        if prop not in ["name", "type", "loc", "css", "props", "sections", "c_type"] {
            if here.context[prop]: props[prop] = here.context[prop];
        }
    }
       
}

walker pre_renderer {
    has anchor payload={};

    page {
        take -->[0];
    }
    

    Component {
        if(here.loc==null): here.loc=payload;
        take -->;
    }

    // with exit {
    //     report payload;
    // }
}

walker create_page {
    has anchor page;
    has page_graph;

    page = spawn node::page --> page_graph;
}


