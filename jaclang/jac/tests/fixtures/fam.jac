# This is a comment
// This is also a commment
"""
These are doc strings and can be used as comments
Use them to document your code
"""

import:jac .stuff;
import:py from .activity, Activity as Actvy;

node location {
    has x: int, y: int, name: str;
    has anchor activities: list[Activity];
    has hidden intro: str = "Welcome";
    has visited: int = 0;


    can record with tourist entry {
        visited+=1;
        for i in activities {
            i.duration = visitor.duration;
            if here.name not in visitor.passport {
                if i.name == "Hiking" {
                    for j=0 to j<3 by j+=1 {
                        i.duration += 1;
                    }
                    i.duration += 1;
                }
                visitor.passport.append(here.name);
               }
        }
    }
}

walker tourist {
    has duration: int;
    has budget: int;
    has passport: list[str];

    can make_visit with location, other exit {
        b=:g:stuff:w:tourist;
        a = spawn :g:stuff:w:tourist;
        a = spawn :w:tourist;
        a = <-[:g:edget:e:myedge|>(=a==1,b==2)]-;
        a = b +[:g:edget:e:myedge|>{a=1}]+> c;
        a = b <+[:g:edget:e:myedge|>{a=1}]+ c;
        a = here +[:g:edget:e:myedge|>{a=1}]+> spawn :g:stuff:n:tourist;
        :g:stuff:w:tourist |> here;
        report here.activities;
    }

    can do_something(app: int =Actvy) -> Actvy {
        app.do_something();
    }
    can do_something(app: int = Actvy, other: float = Actvy) -> Actvy {
        return app?.do_something(other);
    }

    can outside_func() -> None;
}


:walker:tourist:ability:outside_func {

}