---
sidebar_position: 1
---

# Overview

myca is an intelligent platform for personal growth that provides insights and tools to help you become a better you through task and goal tracking.

We'll delve into its implementation in the next few sections.

myca's core data elements represent a calendar of tasks for the user. These include:

- `life`: belongs to a user and holds a collection of years
- `year`: a collection of months
- `month`: a collection of weeks
- `week`: a collection of days
- `day`: a collection of workettes
- `workette`: encapsulates data for a task or goal

They form a hierarchy of time components and tasks. In this model a workette is linked back to the previous uncompleted version of itself and can have sub-workettes which are carried forward. Each day is also linked to the day that came before it.

### Hierarchy Diagram

![Hierarchy Diagram](/img/tutorial/myca-a-jaseci-product/myca_hierarchy_diagram.png)

<!-- TODO: Add link from final docs website -->
Next let’s take a look at the [Jac implementation]('#') of the myca graph.