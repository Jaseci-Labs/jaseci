"""Example of simple walker walking nodes."""
import:py from jac_cloud.core.context {JaseciContext}
import:py from jac_cloud.jaseci.models {User as BaseUser, NO_PASSWORD}
import:py from jac_cloud.jaseci.utils {SendGridEmailer}
import:py from dataclasses {dataclass}
import:py from fastapi {UploadFile}

include:jac simple_graph_mini;

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


:walker:detach_node:can:enter_B {
    return here del --> [-->];
}

:walker:create_nested_node:can:enter_root {
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
    return n;
}

:walker:update_nested_node:can:enter_root {
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
    return nested;
}

:walker:update_nested_node:can:enter_nested {
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
    return here;
}

:walker:detach_nested_node:can:enter_root {
    return here del--> [-->(`?Nested)];
}

:walker:visit_nested_node:can:enter_root {
    nesteds = [-->(`?Nested)];
    if nesteds {
        return [-->(`?Nested)][0];
    } else {
        return nesteds;
    }
}

:walker:visit_nested_node:can:enter_nested {
    return here;
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
                    json={"a": 1, "b": 2},
                    enum_field = Enum.C
                ),
                enum_field = Enum.B
            ),
            enum_field = Enum.A
        );
        here ++> n;
        here.__jac__.apply();

        # simulate no auto save
        jsrc = Jac.get_context().mem;
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
        nested.parent.child.enum_field = Enum.A;
        nested.parent.json["b"] = 2;
        nested.parent.arr.append(2);
        nested.parent.val = 2;
        nested.parent.enum_field = Enum.C;
        nested.json["a"] = 1;
        nested.arr.append(1);
        nested.val = 1;
        nested.enum_field = Enum.B;
        nested.__jac__.apply();

        # simulate no auto save
        jsrc = Jac.get_context().mem;
        jsrc.__mem__.clear();
        jsrc.__gc__.clear();

        return nested;
    }
}

walker manual_detach_nested_node {
    can enter_root with `root entry {
        nested = [-->(`?Nested)][0];
        detached = here del--> [-->(`?Nested)];
        Jac.destroy(nested);
        nested.__jac__.apply();

        # simulate no auto save
        jsrc = Jac.get_context().mem;
        jsrc.__mem__.clear();
        jsrc.__gc__.clear();

        return detached;
    }
}

walker manual_delete_nested_node {
    can enter_root with `root entry {
        nested = [-->(`?Nested)][0];
        Jac.destroy(nested);
        nested.__jac__.apply();

        # simulate no auto save
        jsrc = Jac.get_context().mem;
        jsrc.__mem__.clear();
        jsrc.__gc__.clear();

        report [-->(`?Nested)];
    }
}

walker manual_delete_nested_edge {
    can enter_root with `root entry {
        nested_edge = :e:[-->][0];
        Jac.destroy(nested_edge);
        nested_edge.__jac__.apply();

        # simulate no auto save
        jsrc = Jac.get_context().mem;
        jsrc.__mem__.clear();
        jsrc.__gc__.clear();

        report [-->(`?Nested)];
    }
}

:walker:allow_other_root_access:can:enter_root {
    if self.via_all {
        Jac.unrestrict(here, self.level);
    } else {
        import:py from jac_cloud.core.architype {BaseAnchor}
        Jac.allow_root(here, BaseAnchor.ref(self.root_id), self.level);
    }
}

:walker:allow_other_root_access:can:enter_nested {
    if self.via_all {
        Jac.unrestrict(here, self.level);
    } else {
        import:py from jac_cloud.core.architype {BaseAnchor}
        Jac.allow_root(here, BaseAnchor.ref(self.root_id), self.level);
    }
}

:walker:disallow_other_root_access:can:enter_root {
    if self.via_all {
        Jac.restrict(here);
    } else {
        import:py from jac_cloud.core.architype {BaseAnchor}
        Jac.disallow_root(here, BaseAnchor.ref(self.root_id));
    }
}

:walker:disallow_other_root_access:can:enter_nested {
    if self.via_all {
        Jac.restrict(here);
    } else {
        import:py from jac_cloud.core.architype {BaseAnchor}
        Jac.disallow_root(here, BaseAnchor.ref(self.root_id));
    }
}

walker custom_report {
    can enter1 with `root entry {
        report 1;
        report 2;
        report 3;

        Jac.report({
            "testing": 1
        }, True);
    }

    class __specs__ {
        has auth: bool = False;
    }
}

walker Walker {
    class __specs__ {
        has private: bool = True;
    }
}

node Node {
    has val: str;

    can entry1 with entry {
        return f"{self.val}-2";
    }

    # with 'visit_sequence' (string class reference) is not yet supported
    can entry3 with Walker entry {
        return f"{self.val}-3";
    }

    # with 'visit_sequence' (string class reference) is not yet supported
    can exit1 with Walker exit {
        return f"{self.val}-4";
    }

    can exit2 with exit {
        return f"{self.val}-5";
    }
}
walker visit_sequence:Walker: {
    can entry1 with entry {
        return "walker entry";
    }

    can entry2 with `root entry {
        here ++> Node(val = "a");
        here ++> Node(val = "b");
        here ++> Node(val = "c");
        visit [-->];
        return "walker enter to root";
    }

    can entry3 with Node entry {
        return f"{here.val}-1";
    }

    can exit1 with Node exit {
        return f"{here.val}-6";
    }

    can exit2 with exit {
        return "walker exit";
    }

    class __specs__ {
        has auth: bool = False;
    }
}

#################################################################
#                    TESTING SPAWN WALKER                       #
#################################################################

node NodeTest {
    has value: int;
}

walker WalkerTestSpawn {
    has visited_nodes: list = [];
    has entry_count: int = 0;
    has exit_count: int = 0;

    can walker_entry with entry {
        print("Walker entry: ", here);
        self.entry_count += 1;
    }

    can node_entry with `root entry {
        visit [-->](`?NodeTest);
        print("Node entry: ", here);
    }

    can node_exit with NodeTest exit {
        print("Node exit: ", here);
        self.visited_nodes.append(here);
    }

    can walker_exit with exit {
        print("Walker exit: ", here);
        self.exit_count += 1;
    }
}

with entry {
    for i in range(5) {
        root ++> (next := NodeTest(value=i));
    }
    visitor = root spawn WalkerTestSpawn();
    print("Visited nodes: ", visitor.visited_nodes);
    print("Entry counts: ", visitor.entry_count);
    print("Exit counts: ", visitor.exit_count);
}