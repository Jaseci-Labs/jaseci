---
sidebar_position: 1
description: Jaseci 2.0 Rules of Engagement
title: Rules of Engagement
slug: "/"
---

# Rules of Engagement

## Join Discord and say hi!

https://discord.gg/r5CRtxnPU7

## Every PR must close an issue

In general, create an issue with description before working on a PR. Be sure the PR tags the set of issues it closes. If an issue is missed that is closed, identify the PR that closed it and comment.

Lets keep issues clean and accurate.

## Every PR must have a test and documentation attached

Every PR that is a new feature and/or bug fix must have a test! Refactoring code may get away with not including tests iff it specifies in the description of the PR which test covers it.

Every PR that is a new feature and/or bug fix must have documentation updates to either internals or docs. Small refactors may get exceptions but this must be described in the PRs description.

No exceptions to these rules. If a PR sneaks in that doesn't follow this protocol, it is subject to reversion.

## How to Inject Ideas on Jaseci Improvement/Suggestions

Visit our [Ideas (JSEPs) page](./ideas.md) and follow the process. Everyone is welcome to propose ideas!!

## How to Contribute Code

Visit our  [Codebase Guide](../spec/codebase.md) and follow the process. Everyone is welcome to contribute!!

And remember
```python
from community import fun, you, open_issues

if you.having_fun() in [False, None] and you.engaged() in [False, None]:
    you.take_break() if you.need_break() else you.work_on(
        open_issues.get(fun_factor=fun.HIGH)
    ) if open_issues.find(fun_factor=fun.HIGH) is not None else open_issues.create(
        fun.ANYTHING, start_hack=True
    )
else:
    you.hack_on(leet_code=True)
```