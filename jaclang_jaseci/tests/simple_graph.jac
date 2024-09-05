"""Example of simple walker walking nodes."""
import:py from jaclang_jaseci.core.architype {BaseAnchor}
import:py from jaclang_jaseci.core.context {JaseciContext}
import:py from jaclang_jaseci.jaseci.models {User as BaseUser, NO_PASSWORD}
import:py from jaclang_jaseci.jaseci.utils {SendGridEmailer}
import:py from dataclasses {dataclass}
import:py from fastapi {UploadFile}

class User:BaseUser: {
    has name: str;

    class Collection:BaseUser.Collection: {
        ::py::
        @classmethod
        def __document__(cls, doc) -> "User":
            return User(
                id=doc.pop("_id"),
                email=doc.pop("email"),
                password=doc.pop("password", None) or NO_PASSWORD,
                root_id=doc.pop("root_id"),
                **doc,
            )
        ::py::
    }

    static can send_verification_code(code: str, email: str) -> None {
        SendGridEmailer.send_verification_code(code, email);
    }

    static can send_reset_code(code: str, email: str) -> None {
        SendGridEmailer.send_reset_code(code, email);
    }

    static can sso_mapper(open_id: object) -> dict[str, object] {
        return {
            "name": f"{open_id.first_name} {open_id.last_name}"
        };
    }
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
    has val: int, arr: list, json: dict;
}

obj Parent:Child: {
    has child: Child;
}

node Nested {
    has val: int, arr: list, json: dict, parent: Parent;
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
        return here del --> [-->];
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
                    json={"a": 1, "b": 2}
                )
            ));
        here ++> n;
        return n;
    }
}

walker update_nested_node {
    can enter_root with `root entry {
        nested = [-->(`?Nested)][0];
        nested.parent.child.json["c"] = 3;
        nested.parent.child.arr.append(3);
        nested.parent.child.val = 3;
        nested.parent.json["b"] = 2;
        nested.parent.arr.append(2);
        nested.parent.val = 2;
        nested.json["a"] = 1;
        nested.arr.append(1);
        nested.val = 1;
        return nested;
    }

    can enter_nested with Nested entry {
        here.parent.child.json["c"] = 3;
        here.parent.child.arr.append(3);
        here.parent.child.val = 3;
        here.parent.json["b"] = 2;
        here.parent.arr.append(2);
        here.parent.val = 2;
        here.json["a"] = 1;
        here.arr.append(1);
        here.val = 1;
        return here;
    }
}

walker detach_nested_node {
    can enter_root with `root entry {
        return here del--> [-->(`?Nested)];
    }
}

walker visit_nested_node {
    can enter_root with `root entry {
        nesteds = [-->(`?Nested)];
        if nesteds {
            return [-->(`?Nested)][0];
        } else {
            return nesteds;
        }
    }

    can enter_nested with Nested entry {
        return here;
    }
}

walker manual_create_nested_node {
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
                    json={"a": 1, "b": 2}
                )
            ));
        here ++> n;
        here.__jac__.apply();

        # simulate no auto save
        jsrc = JaseciContext.get().mem;
        jsrc.__mem__.clear();
        jsrc.__gc__.clear();

        return n;
    }
}

walker manual_update_nested_node {
    can enter_root with `root entry {
        nested = [-->(`?Nested)][0];
        nested.parent.child.json["c"] = 3;
        nested.parent.child.arr.append(3);
        nested.parent.child.val = 3;
        nested.parent.json["b"] = 2;
        nested.parent.arr.append(2);
        nested.parent.val = 2;
        nested.json["a"] = 1;
        nested.arr.append(1);
        nested.val = 1;
        nested.__jac__.apply();

        # simulate no auto save
        jsrc = JaseciContext.get().mem;
        jsrc.__mem__.clear();
        jsrc.__gc__.clear();

        return nested;
    }
}

walker manual_detach_nested_node {
    can enter_root with `root entry {
        nested = [-->(`?Nested)][0];
        detached = here del--> [-->(`?Nested)];
        nested.__jac__.destroy();
        nested.__jac__.apply();

        # simulate no auto save
        jsrc = JaseciContext.get().mem;
        jsrc.__mem__.clear();
        jsrc.__gc__.clear();

        return detached;
    }
}

walker delete_nested_node {
    can enter_root with `root entry {
        nested = [-->(`?Nested)][0];
        nested.__jac__.destroy();
        # nested.__jac__.apply();

        report [-->(`?Nested)];
    }
}

walker manual_delete_nested_node {
    can enter_root with `root entry {
        nested = [-->(`?Nested)][0];
        nested.__jac__.destroy();
        nested.__jac__.apply();

        # simulate no auto save
        jsrc = JaseciContext.get().mem;
        jsrc.__mem__.clear();
        jsrc.__gc__.clear();

        report [-->(`?Nested)];
    }
}

walker delete_nested_edge {
    can enter_root with `root entry {
        nested_edge = :e:[-->][0];
        nested_edge.__jac__.destroy();

        report [-->(`?Nested)];
    }
}

walker manual_delete_nested_edge {
    can enter_root with `root entry {
        nested_edge = :e:[-->][0];
        nested_edge.__jac__.destroy();
        nested_edge.__jac__.apply();

        # simulate no auto save
        jsrc = JaseciContext.get().mem;
        jsrc.__mem__.clear();
        jsrc.__gc__.clear();

        report [-->(`?Nested)];
    }
}

walker allow_other_root_access {
    has root_id: str, level: int | str = 0, via_all: bool = False;

    can enter_root with `root entry {
        if self.via_all {
            here.__jac__.unrestrict(self.level);
        } else {
            here.__jac__.allow_root(BaseAnchor.ref(self.root_id), self.level);
        }
    }

    can enter_nested with Nested entry {
        if self.via_all {
            here.__jac__.unrestrict(self.level);
        } else {
            here.__jac__.allow_root(BaseAnchor.ref(self.root_id), self.level);
        }
    }
}

walker disallow_other_root_access {
    has root_id: str, via_all: bool = False;

    can enter_root with `root entry {
        if self.via_all {
            here.__jac__.restrict();
        } else {
            here.__jac__.disallow_root(BaseAnchor.ref(self.root_id));
        }
    }

    can enter_nested with Nested entry {
        if self.via_all {
            here.__jac__.restrict();
        } else {
            here.__jac__.disallow_root(BaseAnchor.ref(self.root_id));
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