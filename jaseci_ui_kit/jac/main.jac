import {*} with './example_site.jac';

walker get_props {
    has anchor props = {};

    for prop in here.context.dict::keys {
        if prop not in ["name", "type", "loc", "css", "props", "sections", "c_type"] {
            if here.context[prop]: props[prop] = here.context[prop];
        }
    }
       
}

walker pre_renderer {
    has payload={};

    Component {
        if(here.loc==null): here.loc=payload;
        take -->;
    }

    with exit {
        std.out(payload);
    }
}

walker init {
    // Spawn main graph at root
    root {
        spawn here -[section(name="root")]-> graph::my_site;
        spawn -->[0] walker::pre_renderer;
    }
}




