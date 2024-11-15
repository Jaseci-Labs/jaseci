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

    static can system_admin_default() -> dict[str, object] {
        return {
            "name": f"System Administrator"
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

:walker:check_populated_graph:can:enter {
    import:py from jac_cloud.core.architype {NodeAnchor, EdgeAnchor, WalkerAnchor}

    id = here.__jac__.id;
    count = NodeAnchor.Collection.count({"$or": [{"_id": id}, {"root": id}]});
    count += EdgeAnchor.Collection.count({"root": id});
    count += WalkerAnchor.Collection.count({"root": id});

    report count;
}