# This is a comment
// This is also a commment
"""
These are doc strings and can be used as comments
Use them to document your code
"""

import:jac .stuff;
import:py from .activity, Activity as Actvy;

node location {
    has x: int, y:int, name:str;
    has anchor activities: list[Activity];
    has hidden intro: str = "Welcome";
    // has int visited = 0;
    //

    // can record with tourist entry {
    //     visited+=1;
    //     for i in activities {
    //         i.duration = visitor.duration;
    //         if here.name not in visitor.passport {
    //             visitor.passport.append(here.name);
    //            }
    //     }
    // }
}

walker tourist {
    // has int duration;
    // has int budget;
    // has passport: list[str];

    // can visit with location exit {
    //     report here.activities;
    // }
}