# This is a comment

#*
This is multi line comment
Many styles!
*#
"""
These are doc strings and can be used as comments
Use them to document your code
"""

import:jac stuff;
import:py from .activity, Activity as Actvy;

node location {
    has x: int,
        y: int,
        name: str = True;
    has activities: list[Activity];
    has intro: str = "Welcome";
    has visited: int = 0;

    can record with tourist entry {
        visited+=1;

        for i in activities {
            i.duration = visitor.duration;
            if here.name not in visitor.passport {
                if i.name == "Hiking" {
                    for j=0 to j<3 by j+=1  {
                        i.duration+=1;
                    }
                    i.duration+=1;
                }
                visitor.passport.append(here.name);
            }
        }
    }
}

walker tourist {
    has duration: float = .435e-2;
    has budget: int;
    has passport: list[str];

    can make_visit with location | other exit {
        b = tourist;
        a = spawn tourist;
        a = [<-:myedge:a == 1, b == 2:-];
        a = b +:myedge:a=1:+> c;
        a = b <+:myedge:a=1:+ c;
        a = here +:myedge:a=1:+> spawn tourist;
        tourist |> here;
        report here.activities;
    }

    can do_something(app: int=Actvy) -> Actvy {
        app.do_something();
    }

    can do_something(app: int=Actvy, other: float=Actvy) -> Actvy {
        return app?.do_something(other);
    }
    can outside_func() -> None;
}

:walker:tourist:can:outside_func {}
