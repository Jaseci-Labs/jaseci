# The Very Basics: CLI vs Shell-mode, and Session Files

## Shell Mode 

In shell mode, all of the same Jaseci API functionality is available within a single session. To invoke shell-mode, simply execute jsctl without any commands and jsctl will enter shell mode as per the example below. Session Files At this point, it’s important to understand how sessions work. In a nutshell, a session captures the complete state of a jaseci machine. This state includes the status of memory, graphs, walkers, configurations, etc. The complete state of a Jaseci machine can be captured in a .session file. Every time state changes for a given session via the jsctl tool the assigned session file is updated. Additionally, jaseci masters have the choice of selecting which session file they want to use with the following command.

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
```
haxor@linux:~/jaseci# ls *.session
js.session
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
}
]
haxor@linux:~/jaseci#
```
```
haxor@linux:~/jaseci# jsctl -f mynew.session graph list
[]
haxor@linux:~/jaseci# ls *.session
js.session mynew.session
haxor@linux:~/jaseci#
```

## In-memory mode

It's crucial to keep in mind that there is an in-memory mode that can be activated by using the -m or --mem-only flags. This option is ideal when you want to experiment with a machine in shell-mode or when you need to run a script in Jac without maintaining machine state after completion. Throughout this chapter, you will see the in-memory session mode being used frequently, giving you a better understanding of its usage. 

## CLI Mode

It's crucial to acknowledge that with CLI mode, jaseci administrators have the option to execute commands without retaining a session file or utilising the in-memory mode. 
