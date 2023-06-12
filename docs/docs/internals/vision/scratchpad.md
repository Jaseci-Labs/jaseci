---
sidebar_position: 4
description: Scratchpad for ideas and thoughts
title: Scratchpad
---

Brainstorm Code Snippet

```jac
# This is a comment
// This is also a commment
"""
These are doc strings and can be used as comments
Use them to document your code
"""

import:jac .stuff;
import:py from .activity, Activity as Actvy;

node location:super:blah {
    has x: int, y: int, name: str;
    has anchor activities: list[Activity];
    has hidden intro: str = "Welcome";
    has visited: int = 0;


    can record with tourist entry {
        visited+=1;
        for i in activities {
            i.duration = visitor.duration;
            if here.name not in visitor.passport {
                visitor.passport.append(here.name);
               }
        }
    }
}

walker tourist {
    has duration: int;
    has budget: int;
    has passport: list[str];

    can visit with location, other exit {
        visit -->;
        if here.visited == 0 {
            print here.intro;
        }
        report here.activities;
    }
}
```

I am designing a computational runtime stack called Jaseci, and a language for the stack called Jac that uses a new programming model I coined as data-spatial programming. I'm writing the design specifications for the next version of Jaseci and Jac. Can you generate clear, concise, and technial specification and justification in markdown that conveys the following:

I'm writing a full specification for a programming language I've created called Jac that implements an new programming model called data spatial programming. Can you write a section of this spec in markdown covering the following points: