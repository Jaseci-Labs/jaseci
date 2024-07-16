"""Example of simple walker walking nodes."""
import:py from jaclang_jaseci, FastAPI;
import:py from jaclang_jaseci.core.types, File, Files, OptFile, OptFiles;
import:py from jaclang_jaseci.jaseci.models, User as BaseUser;
import:py from jaclang_jaseci.plugin, specs;
import:py from jaclang_jaseci.jaseci.utils, SendGridEmailer;

node GrandParent {
    has name: str, age: int;
}

node Parent {
    has name: str, age: int;
}

node Child {
    has name: str, age: int;
}

@specs(path = "will-be-ignored-because-of-inner-class-Specs")
walker create_sample_graph {
    async can enter with `root entry {
        g = GrandParent(name="lola", age=65);
        p = Parent(name="mama", age=65);
        c = Child(name="daughter", age=65);
        here ++> g;
        g ++> p;
        p ++> c;
        await here.__jac__.save();
    }

    obj __specs__ {}
}

with entry:__main__ {
    # SendGridEmailer.start();
    FastAPI.start(
        host="0.0.0.0",
        port=8001
    );
}