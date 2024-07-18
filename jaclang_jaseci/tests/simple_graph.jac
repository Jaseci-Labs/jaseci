"""Example of simple walker walking nodes."""
import:py from jaclang_jaseci, FastAPI;
import:py from jaclang_jaseci.plugin, specs;
import:py from jaclang_jaseci.jaseci.models, User as BaseUser, NO_PASSWORD;
import:py from jaclang_jaseci.jaseci.utils, SendGridEmailer;
import:py from dataclasses, dataclass;

::py::
class User(BaseUser):
    name: str

    class Collection(BaseUser.Collection):
        @classmethod
        def __document__(cls, doc) -> "User":
            return User.model()(
                id=str(doc.pop("_id")),
                email=doc.pop("email"),
                password=doc.pop("password", None) or NO_PASSWORD,
                root_id=str(doc.pop("root_id")),
                **doc,
            )

    @staticmethod
    def send_verification_code(code: str, email: str) -> None:
        """Send verification code."""
        SendGridEmailer.send_verification_code(code, email)

    @staticmethod
    def send_reset_code(code: str, email: str) -> None:
        """Send reset code."""
        SendGridEmailer.send_reset_code(code, email)

    @staticmethod
    def sso_mapper(open_id) -> dict[str, object]:
        """Send verification code."""
        return {
            "name": f"{open_id.first_name} {open_id.last_name}"
        }


@dataclass
class Child:
    val: int
    arr: list
    json: dict

@dataclass
class Parent(Child):
    child: Child

::py::

node A {
    has val: int;
}

node B {
    has val: int;
}

node C {
    has val: int;
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

    obj __specs__ {}
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

    obj __specs__ {}
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
                    arr=[2],
                    json={"B": 2}
                )
            ));
        here ++> n;
        return n;
    }
}

walker update_nested_node {
    can enter_root with `root entry {
        nested = [-->Nested][0];
        nested.parent.child.json["c"] = 3;

        report nested;
    }
}

with entry:__main__ {
    # SendGridEmailer.start();
    FastAPI.start(
        host="0.0.0.0",
        port=8001
    );
}