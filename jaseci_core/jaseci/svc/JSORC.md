## JSORC Action Optimizer

### What is JSORC?
JSORC is short for the JaSeci ORChestrator.
It is a key component of the jaseci runtime system that oversees the various components and services of the Jaseci runtime system.

### Jaseci Actions
Jaseci actions are extension to the core Jaseci runtime.
Jaseci actions are used to introduce external libraries and functionalities to your jaseci applications.
Examples include AI models and useful python packages (such as numpy and scipy).
As a jaseci developer, one can use the standard jaseci action APIs to load and unlod actions.
Refer to the actions section of the jaseci documentation for more details.

### Why do we need JSORC?
With standard actions APIs, developers need to manually make decision on whether the action should be a local action or remote action and explictly manage any remote instances if needed.
This introduces complexity for the developers as well as potential impact on performance.
JSORC solves this by subsuming this responsibility and automatically manage actions based on its observations of the state of the runtime system.

### JSORC API details
With JSORC, we introduce a new set of APIs for loading and unloading actions:

- jsorc_actions_load
- jsorc_actions_status
- jsorc_actions_unload
- jsorc_actions_config

A set of APIs for setting a custom actions management policy

- jsorc_actionpolicy_set
- jsorc_actionpolicy_get

There are also a set of APIs for performance tracking and becnhmarking:

- jsorc_trackact_start/stop
- jsorc_becnhmark_start/stop/report
- jsorc_tracksys_start/stop/report
- jsorc_loadtest

### JSORC Architecture

### Relevant Source Code

### Todos
* Include jaseci-db in JSORC's purview