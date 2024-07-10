"""Example of simple walker walking nodes."""
import:py from jaclang_jaseci, FastAPI;
import:py from jaclang_jaseci.core.types, File, Files, OptFile, OptFiles;
import:py from jaclang_jaseci.core.model, User as BaseUser;
import:py from jaclang_jaseci.plugin.jaseci, specs;
import:py from jaclang_jaseci.core.mail, SendGridEmailer;

node boy {
    has val1: str, val2: str;
}

node girl {
    has val: str;
}

node someone {
    has val: list = [];
}

@specs(path = "will-be-ignored-because-of-inner-class-Specs")
walker create_sample_graph {
    can enter with `root entry {
        b = boy(val1="a", val2="b");
        g = girl(val="b");
        b ++> g;
        root ++> b;
        return True;
    }

    obj Specs {}
}

@specs
walker visit_sample_graph {
    can enter1 with `root entry {
        report root;
        boys = [-->];
        report boys[0];
        visit boys;
        return 1;
    }

    can enter2 with boy entry {
        girls = [-->];
        report girls[0];
        visit girls;
        return 2;
    }

    can enter3 with girl entry {
        anyone = [-->];
        report anyone;
        visit anyone;
        return 3;
    }
}

walker update_sample_graph {
    can enter1 with `root entry {
        boys = [-->];
        visit boys;
    }

    can enter2 with boy entry {
        old = [-->];
        report old[0];

        new = girl(val="new");
        here ++> new;

        here del--> old[0];

        report ([-->])[0];
    }

    obj Specs {}
}

walker delete_sample_graph {
    can enter1 with `root entry {
        boys = [-->];
        visit boys;
    }

    can enter2 with boy entry {
        old = [-->];
        report old[0];

        new = girl(val="latest");
        here ++> new;

        old[0].destroy();

        report ([-->])[0];
    }

    obj Specs {}
}

walker create_list_field {
    can enter1 with `root entry {
        a = someone();
        root ++> a;
        report a;
    }
    obj Specs {}
}

walker update_list_field {
    can enter2 with someone entry {
        here.val.append(1);
        report here;

        visit [-->];
    }

    obj Specs {}
}

walker get_list_field {
    can enter2 with someone entry {
        report here;
        report [-->];
    }

    obj Specs {}
}

walker allow_other {
    has root_id: str = None, node_id: str = None, write: bool = False;

    can enter2 with someone entry {
        if self.root_id {
            here.allow_root(DocAnchor.ref(self.root_id), self.write);
        }
        if self.node_id {
            here.allow_node(DocAnchor.ref(self.node_id), self.write);
        }
        report here;
    }

    obj Specs {}
}

walker disallow_other {
    has root_id: str = None, node_id: str = None;

    can enter2 with someone entry {
        if self.root_id {
            here.disallow_root(DocAnchor.ref(self.root_id));
        }
        if self.node_id {
            here.disallow_node(DocAnchor.ref(self.node_id));
        }

        report here;
    }

    obj Specs {}
}

walker connect_other_node {
    has node_id: str = None;

    can enter2 with someone entry {
        if self.node_id {
            other_node = DocAnchor.ref(self.node_id).connect(here);
            here ++> other_node;

        }
        report here;
    }

    obj Specs {}
}

@specs
walker post_no_body {}

walker post_with_body {
    has a: str;
}

walker get_no_body {
    obj Specs {
        static has methods: list = ["get"];
    }
}

walker get_with_query {
    has a: str;

    obj Specs {
        static has methods: list = ["get"], as_query: list = ["a"];
    }
}

walker get_all_query {
    has a: str;
    has b: str;

    obj Specs {
        static has methods: list = ["get"], as_query: list = "*", auth: bool = False;
    }
}

walker combination {
    has a: str;
    has b: str;
    has c: str;

    obj Specs {
        static has methods: list = ["post", "get"], as_query: list = ["a", "b"];
    }
}

walker post_path_var {
    has a: str;

    obj Specs {
        static has path: str = "/{a}", methods: list = ["post", "get"];
    }
}

walker combination2 {
    has a: str;
    has b: str;
    has c: str;

    obj Specs {
        static has path: str = "/{a}", methods: list = ["post", "get", "put", "patch", "delete", "head", "trace", "options"], as_query: list = ["b"];
    }
}

walker post_with_file {
    has single: File;
    has multiple: Files;
    has singleOptional: OptFile = None;
    has multipleOptional: OptFiles = None;


    can enter with `root entry {
        print(self.single);
        print(self.multiple);
        print(self.singleOptional);
        print(self.multipleOptional);
    }

    obj Specs {}
}

walker post_with_body_and_file {
    has val: int;
    has single: File;
    has multiple: Files;
    has optional_val: int = 0;

    can enter with `root entry {
        print(self.val);
        print(self.optional_val);
        print(self.single);
        print(self.multiple);
    }

    obj Specs {
        static has auth: bool = False;
    }
}

walker nested1 {
    has sample: str = "";
    can enter with `root entry {
        self.sample = "nested1";
    }

    obj Specs {
        static has private: bool = True;
    }
}

walker nested2 {
    can enter with `root entry {
        wlk = here spawn nested1();
        report wlk.sample;
        report "nested2";
    }

    obj Specs {
        static has auth: bool = False;
    }
}

with entry:__main__ {
    # SendGridEmailer.start();
    FastAPI.start(
        host="0.0.0.0",
        port=8001
    );
}