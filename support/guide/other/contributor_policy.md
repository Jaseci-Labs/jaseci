# How to Be a Jaseci-tributor

There are two classes of contributors to Jaseci, *casual contributors* and *committed contributors*. This section defines each group and outlines the general guidelines for both.

## The Casual Jaseci-tributor

A casual contributor is one that is passionate about or otherwise interested in Jaseci or Jac and would like to improve the Jaseci ecosystem in some way. They make their contribution of time, energy, and most importantly, their brain juice for the betterment of Jaseci hackers everywhere. We welcome you! And thanks in advance!

### General Guidelines

- Create and Issue, spark a discussion, or simply lob a PR our way with description/rational and we'll merge and/or improve upon then merge anything that makes sense for a better Jaseci.
- We like to have a test and some documentation (even if brief) for any changes for which they may be relevant, certainly not a deal breaker though. If your contribution is important, another casual or committed contributor can help.
- Thats pretty much it, we like to make friends in the Jaseci community so we hope to hear from you no matter what the idea/contribution is. Everything is more fun with friends!

## The Committed Jaseci-tributor

A committed contributor is one that is on the TOTC (*team of the committed*). TOTC members in some way sustains themselves by being a contributor to Jaseci. This comes about in a number of ways, whether it be funded from donations, funding from government grants, being dedicated to the TOTC by some employer, or a volunteer that would like to dedicate themselves to TOTC roadmap items (i.e., be relied upon by other TOTC contributors).

> **Note**
>
> The TOTC is an open group. We accept members from all across the world that can take the TOTC oath which we fit in to 1 sentence. Oath: *I will strive my very best to be a good human, be reliable, share my ideas without reservation, be patient when they aren't accepted right away, follow the guidelines, suggest improvements instead of get resentful, and take breaks when I'm not having fun.*

### Guidelines

1. Come to the meetings or share in relevant Slack channel a note before, or we will worry insensently that something is terribly wrong
2. For a given thing (e.g., task, todo, doc, note, comment, delegation, request for help, etc), it exists iff it is present in our system of Objective and Centralized Truth (OCT for short, aka Click-Up atm, links to other systems like github, and google docs are ok).
3. For the days committed to work, if nothing is checked off, leave a little comment on how things went iff nothing gets checked off that day.
4. And most importantly!! **Follow Below!**
```python
from work import fun, you, open_prs

if you.having_fun() in [False, None] and you.engaged() in [False, None]:
    you.take_break() if you.need_break() else you.work_on(
        open_prs.get(fun_factor=fun.HIGH)
    ) if open_prs.find(fun_factor=fun.HIGH) is not None else open_prs.create(
        fun.ANYTHING, start_hack=True
    )
else:
    you.hack_on(leet_code=True)
```