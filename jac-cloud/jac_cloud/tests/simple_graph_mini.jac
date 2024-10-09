"""Example of simple walker walking nodes."""
import:py from fastapi {UploadFile}
import:py from uuid {UUID}

enum Enum {
    A = "a",
    B = "b",
    C = "c"
}

node A {
    has val: int;
}

node B {
    has val: int;
}

node C {
    has val: int;
}

obj Child {
    has val: int, arr: list, json: dict, enum_field: Enum;
}

obj Parent:Child: {
    has child: Child;
}

node Nested {
    has val: int, arr: list, json: dict, parent: Parent, enum_field: Enum;
}

walker create_graph {
    can enter_root with `root entry {
        a = A(val=0);
        b = B(val=1);
        c = C(val=2);
        here ++> a;
        a ++> b;
        b ++> c;

        report here;
        report a;
        report b;
        report c;
    }
}

walker traverse_graph {
    can enter with `root entry {
        report here;
        visit [-->];
    }

    can enter_A with A entry {
        report here;
        visit [-->];
    }

    can enter_B with B entry {
        report here;
        visit [-->];
    }

    can enter_C with C entry {
        report here;
    }
}

walker detach_node {
    can enter with `root entry {
        visit [-->];
    }

    can enter_A with A entry {
        visit [-->];
    }

    can enter_B with B entry {
        report here del --> [-->];
    }
}

walker update_graph {
    can enter with `root entry {
        report here;
        visit [-->];
    }

    can enter_A with A entry {
        here.val = 1;
        report here;
        visit [-->];
    }

    can enter_B with B entry {
        here.val = 2;
        report here;
        visit [-->];
    }
}

walker create_nested_node {
    can enter_root with `root entry {
        n = Nested(
            val=0,
            arr=[],
            json={},
            parent=Parent(
                val=1,
                arr=[1],
                json={"a": 1},
                child=Child(
                    val=2,
                    arr=[1, 2],
                    json={"a": 1, "b": 2},
                    enum_field = Enum.C
                ),
                enum_field = Enum.B
            ),
            enum_field = Enum.A
        );
        here ++> n;
        report n;
    }
}

walker update_nested_node {
    can enter_root with `root entry {
        nested = [-->(`?Nested)][0];
        nested.parent.child.json["c"] = 3;
        nested.parent.child.arr.append(3);
        nested.parent.child.val = 3;
        nested.parent.child.enum_field = Enum.A;
        nested.parent.json["b"] = 2;
        nested.parent.arr.append(2);
        nested.parent.val = 2;
        nested.parent.enum_field = Enum.C;
        nested.json["a"] = 1;
        nested.arr.append(1);
        nested.val = 1;
        nested.enum_field = Enum.B;
        report nested;
    }

    can enter_nested with Nested entry {
        here.parent.child.json["c"] = 3;
        here.parent.child.arr.append(3);
        here.parent.child.val = 3;
        here.parent.child.enum_field = Enum.A;
        here.parent.json["b"] = 2;
        here.parent.arr.append(2);
        here.parent.val = 2;
        here.parent.enum_field = Enum.C;
        here.json["a"] = 1;
        here.arr.append(1);
        here.val = 1;
        here.enum_field = Enum.B;
        report here;
    }
}

walker detach_nested_node {
    can enter_root with `root entry {
        report here del--> [-->(`?Nested)];
    }
}

walker visit_nested_node {
    can enter_root with `root entry {
        nesteds = [-->(`?Nested)];
        if nesteds {
            report [-->(`?Nested)][0];
        } else {
            report nesteds;
        }
    }

    can enter_nested with Nested entry {
        report here;
    }
}

walker delete_nested_node {
    can enter_root with `root entry {
        nested = [-->(`?Nested)][0];
        Jac.destroy(nested);
        # nested.__jac__.apply();

        report [-->(`?Nested)];
    }
}

walker delete_nested_edge {
    can enter_root with `root entry {
        nested_edge = :e:[-->][0];
        Jac.destroy(nested_edge);

        report [-->(`?Nested)];
    }
}

walker allow_other_root_access {
    has root_id: str, level: int | str = 0, via_all: bool = False;

    can enter_root with `root entry {
        if self.via_all {
            here.__jac__.unrestrict(self.level);
        } else {
            here.__jac__.allow_root(UUID(self.root_id), self.level);
        }
    }

    can enter_nested with Nested entry {
        if self.via_all {
            here.__jac__.unrestrict(self.level);
        } else {
            here.__jac__.allow_root(UUID(self.root_id), self.level);
        }
    }
}

walker disallow_other_root_access {
    has root_id: str, via_all: bool = False;

    can enter_root with `root entry {
        if self.via_all {
            here.__jac__.restrict();
        } else {
            here.__jac__.disallow_root(UUID(self.root_id));
        }
    }

    can enter_nested with Nested entry {
        if self.via_all {
            here.__jac__.restrict();
        } else {
            here.__jac__.disallow_root(UUID(self.root_id));
        }
    }
}

#################################################################
#                    ENDPOINT CUSTOMIZATIONS                    #
#################################################################

walker post_no_body {}

walker post_with_body {
    has a: str;
}

walker get_no_body {
    class __specs__ {
        has methods: list = ["get"];
    }
}

walker get_with_query {
    has a: str;

    class __specs__ {
        has methods: list = ["get"], as_query: list = ["a"];
    }
}

walker get_all_query {
    has a: str;
    has b: str;

    class __specs__ {
        has methods: list = ["get"], as_query: list = "*", auth: bool = False;
    }
}

walker post_path_var {
    has a: str;

    class __specs__ {
        has path: str = "/{a}", methods: list = ["post", "get"];
    }
}

walker combination1 {
    has a: str;
    has b: str;
    has c: str;

    class __specs__ {
        has methods: list = ["post", "get"], as_query: list = ["a", "b"];
    }
}


walker combination2 {
    has a: str;
    has b: str;
    has c: str;

    class __specs__ {
        has path: str = "/{a}", methods: list = ["post", "get", "put", "patch", "delete", "head", "trace", "options"], as_query: list = ["b"];
    }
}

walker post_with_file {
    has single: UploadFile;
    has multiple: list[UploadFile];
    has singleOptional: UploadFile | None = None;


    can enter with `root entry {
        print(self.single);
        print(self.multiple);
        print(self.singleOptional);
    }

    class __specs__ {}
}

walker post_with_body_and_file {
    has val: int;
    has single: UploadFile;
    has multiple: list[UploadFile];
    has optional_val: int = 0;

    can enter with `root entry {
        print(self.val);
        print(self.optional_val);
        print(self.single);
        print(self.multiple);
    }

    class __specs__ {
        has auth: bool = False;
    }
}


walker custom_status_code {
    has status: int;

    can enter with `root entry {
        Jac.get_context().status = self.status;
    }
}