---
sidebar_position: 2
---

# The very basics

## CLI vs Shell-mode, and Session Files

`jsctl` gives us full access to the Jaseci core APIs via the Command Line of via a shell mode. Lets take a look.

In shell mode, all of the same Jaseci API functionality is available within a single session.

to enter shell mode simply type: `jsctl` at the terminal without any arguments.
 
 Here is an example of shell mode:

 ```
 haxor@linux:~/jaseci# jsctl
Starting Jaseci Shell...
jaseci > graph create
{
  "context": {},
"anchor": null,
"name": "root",
"kind": "generic",
"jid": "urn:uuid:ef1eb3e4-91c3-40ba-ae7b-14c496f5ced1",
"j_timestamp": "2021-08-15T15:15:50.903960",
"j_type": "graph"
}
jaseci > exit
haxor@linux:~/jaseci#
```

In the above we launched `jsctl` directly into shell mode for a single session and we can issue various calls to the `Jaseci` API for that session. In this example we issue a single call to `graph create`, which creates a graph within the Jaseci session with a single root node, then exit the shell with `exit`.

But, we don't always need to enter shell mode to execute commands we can use the CLI mode instead, like this:

```
haxor@linux:~/jaseci# jsctl graph create
{
  "context": {},
"anchor": null,
"name": "root",
"kind": "generic",
"jid": "urn:uuid:91dd8c79-24e4-4a54-8d48-15bee52c340b",
"j_timestamp": "2021-08-15T15:40:12.163954",
"j_type": "graph"
}
haxor@linux:~/jaseci#

```

### Session Files

The Jaseci machine uses session files to keep track of:
- Memory
- Graphs
- Walkers
- Configurations etc.

The complete state of a jaseci machine is captured in a .session file. Every time state changes for a given session via the jsctl tool, the assigned session file gets updated.

If you have been following so far, you can list all the .session files by running the following command:

```
ls *.session
```

This would output: 

```
js.session
```

So if we did not specifically create a session file, this one is created by default by Jaseci.

Remember the create graphs commands we ran earlier when discussing cli and shell mode? Well, Jaseci was actually keeping track of the graphs in its .session file. Its important to note that the same .session file is used across both the Shell and CLI mode.

If we run the following command:

```
jsctl graph list
```

We can see the two graphs:

```
haxor@linux:~/jaseci# jsctl graph list
[
{
"context": {},
"anchor": null,
"name": "root",
"kind": "generic",
"jid": "urn:uuid:ef1eb3e4-91c3-40ba-ae7b-14c496f5ced1",
"j_timestamp": "2021-08-15T15:55:15.030643",
"j_type": "graph"
},
{
  "context": {},
"anchor": null,
"name": "root",
"kind": "generic",
"jid": "urn:uuid:91dd8c79-24e4-4a54-8d48-15bee52c340b",
"j_timestamp": "2021-08-15T15:55:46.419701",
"j_type": "graph"
} ]
haxor@linux:~/jaseci#

```

### Specifying a new `.session` file

To use a different session file (one of our choice), we can use the following command:

```
jsctl -f mynew.session graph list
```

```
haxor@linux:~/jaseci# jsctl -f mynew.session graph list
[]
haxor@linux:~/jaseci# ls *.session
js.session mynew.session
haxor@linux:~/jaseci#

```

>**-f** or --**filename** flag is used to specify the session file to use.

Notice that an empty array is returned. This is the case because our new session file is not aware of the graphs that were created.

If we specify now type:

```
jsctl --filename js.session graph list

```

We can see the two graph objects, since they were saved to `js.session`


### In-memory mode

Its important to note that there is also an in-memory mode that can be created buy using the `-m` or `--mem-only` flags. This flag is particularly useful when you’d simply like to tinker around with a machine in shell-mode or you’d like to script some behavior to be executed in Jac and have no need to maintain machine state after completion. We will be using in memory session mode quite a bit, so you’ll get a sense of its usage throughout this chapter. Next we actually see a workflow for tinkering.




