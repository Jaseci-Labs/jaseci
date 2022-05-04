---
sidebar_position: 3
---

# A simple workflow for Tinkering

As you get to know `Jaseci` and `Jac`, you’ll want to try things and tinker a bit. 

In this section, we’ll get to know how `jsctl` can be used as the main platform for this play. 

A typical flow will involve jumping into shell-mode, writing some code, running that code to observe output, and in visualizing the state of the graph, and rendering that graph in dot to see it’s visualization.

### Installing Graphvis

Before we jump right in, let me strongly encourage you install Graphviz. Graphviz is open source graph visualization software package that includes a handy dandy command line tool call dot. 

**`Dot`** is also a standardized and open graph description language that is a key primitive of Graphviz. 
The `dot` tool in `Graphviz` takes `dot` code and renders it nicely. 

##### Ubuntu:
```
sudo apt install graphviz
```

#### MacOS:
```
brew install graphviz
```

### Writing a simple Jac program

Lets hop into a shell

```
haxor@linux:~/jaseci# jsctl -m
Starting Jaseci Shell...
jaseci >

```

Notice that we used `-m` to create an in-memory session so no session file will be created or saved. Hence, the state of the `Jaseci` machine we run our toy program on doesn't matter to us.

First thing, Lets create a blank graph.

> Remember, all walkers, Jaseci’s primary unit of computation, must run on a node. As default, we can use the root node of a freshly created graph, hence we need to create a base graph.

If you have forgotten how we created our initial graph using `jsctl`. Let’s navigate the help menu to jog our memories.

```
jaseci > help
Documented commands (type help <topic>):
========================================
alias check dev graph ls sentinel
architype config edit login object walker
Undocumented commands:
======================
exit help quit
jaseci > help graph
Usage: graph [OPTIONS] COMMAND [ARGS]...
Group of ‘graph‘ commands
Options:
--help Show this message and exit.
Commands:
  active Group of ‘graph active‘ commands
create Create a graph instance and return root node graph object
delete Permanently delete graph with given id
get Return the content of the graph with format Valid modes:...
list Provide complete list of all graph objects (list of root node...
node Group of ‘graph node‘ commands
jaseci > graph create --help
Usage: graph create [OPTIONS]
Create a graph instance and return root node graph object
Options:
  -o, --output TEXT Filename to dump output of this command call.
-set_active BOOLEAN
--help Show this message and exit.
jaseci >

```

After using `help` from the shell we were able to navigate to the relevant info for `graph create`. Let’s use this newly gotten wisdom.

```
jaseci > graph create -set_active true
{
  "context": {},
"anchor": null,
"name": "root",
"kind": "generic",
"jid": "urn:uuid:7aa6caff-7a46-4a29-a3b0-b144218312fa",
"j_timestamp": "2021-08-15T21:34:31.797494",
"j_type": "graph"
}
jaseci >

```

With this command a graph is created and a single root node is born. `jsctl` shares with us the details of this root graph node. In `Jaseci`, graphs are referenced by their root nodes and every graph has a single root node.

Notice we’ve also set the `-set active` parameter to true. This parameter informs Jaseci to use the root node of this graph (in particular the UUID of this root node) as the default parameter to all future calls to `Jaseci` Core APIs that have a parameter specifying a graph or node to operate on. This global designation that this graph is the `active` graph is a convenience feature so we the user doesn’t have to specify this parameter for future calls. Of course this can be overridden, more on that later.

### Using the built in editor... or use your favorite

Next, lets write some `Jac` code for our little program. `jsctl` has a built in editor that is simple yet powerful. You can use either this built in editor, or your favorite editor to create the `.jac` file for our toy program. 

Let’s use the built in editor.

```
jaseci > edit fam.jac

```

The edit command invokes the built in editor. Though it’s a terminal editor based on ncurses, you can basically use it much like you’d use any wysiwyg editor with features like standard cut `ctrl-c` and paste `ctrl-v`, mouse text selection, etc. For more detailed help cheat sheet see Appendix C. If you must use your own favorite editor, simply be sure that you save the fam.jac file in the same working directory from which you are running the Jaseci shell. 

Now type out the toy program in Jac Code:

```jac
node man;
node woman;
edge mom;
edge dad;
edge married;
walker create_fam {
root {
    spawn here --> node::man;
spawn here --> node::woman;
--> node::man <-[married]-> --> node::woman;
take -->; }
woman {
    son = spawn here <-[mom]- node::man;
son -[dad]-> <-[married]->;
}
man {
    std.out("I␣didn’t␣do␣any␣of␣the␣hard␣work.");
} }

```

Don’t worry if that look a little strange. For now, lets tinker around. Now save and quit the editor. 
If you are using the built in editor thats simply:

```
ctrl-s
ctrl-q combo
```

Ok, now we should have a `fam.jac` file saved in our working directory. 
We can check from the Jaseci shell!

```
jaseci > ls
fam.jac
jaseci >

```

### Listing files
We can list files from the shell prompt. 

By default the ls command only lists files relevant to Jaseci (i.e., *.jac, *.dot, etc). 

To list all files simply add a `--all` or `-a`.

```
jaseci > ls -a

```

### Registering a sentinel

A sentinel is the abstraction Jaseci uses to encapsulate compiled walkers and architype nodes and edges. You can think of registering a sentinel as compiling your jac program.

The walkers of a given sentinel can then be invoked and run on arbitrary nodes
of any graph.

Registering our Jac toy program:

```
jaseci > sentinel register -name fam -code fam.jac -set_active true
2021-08-15 18:03:38,823 - INFO - parse_jac_code: fam: Processing Jac code...
2021-08-15 18:03:39,001 - INFO - register_code: fam: Successfully registered code
{
  "name": "fam",
"kind": "generic",
"jid": "urn:uuid:cfc9f017-cb6c-4d06-bc45-758289c96d3f",
"j_timestamp": "2021-08-15T22:03:38.823651",
"j_type": "sentinel"
}
jaseci >

```

- First, we see some logging output that informs us that the Jac code is being processed (which really means the Jac program is being parsed and IR being generated)

If there are any syntax errors or other issues, this is where the error output will be printed along with any problematic lines of code and such.

- Secondly, If all goes well, we see the next logging output that the code has been successfully registered.

>Note, that we’ve also made this the “active” sentinel meaning it will be used as the default setting for any calls to Jaseci Core APIs that require a sentinel be specified. At this point, Jaseci has registered our code and we are ready to run walkers!

But first, lets take a quick look at some of the objects loaded into our Jaseci machine. For this I’ll briefly introduce the alias group of APIs.

```
jaseci > alias list
{
"sentinel:fam": "urn:uuid:cfc9f017-cb6c-4d06-bc45-758289c96d3f",
"fam:walker:create_fam": "urn:uuid:17598be7-e14f-4000-9d85-66b439fa7421",
"fam:architype:man": "urn:uuid:c366518d-3b1e-41a3-b1ba-0b9a3ce6e1d6",
"fam:architype:woman": "urn:uuid:7eb1c510-73ca-49eb-96aa-34357f77b4cb",
"fam:architype:mom": "urn:uuid:8c9d2a66-4954-4d11-8109-a36b961eeea1",
"fam:architype:dad": "urn:uuid:d80111e4-62e2-4694-bfaa-f3294d9520d8",
"fam:architype:married": "urn:uuid:dc4974df-ea57-406e-9468-a1aa5260d306"
}
jaseci >

```

The `alias` set of APIs are designed as an additional set of convenience tools to simplify the referencing of various objects (walkers, architypes, etc) in Jaseci. Instead of having to use the UUIDs to reference each object, an alias can be used to refer to any object. These aliases can be created or removed utilizing the `alias` APIs.


Upon registering a sentinel, a set of aliases are automatically created for each object produced from processing the corresponding Jac program. The call to alias list lists all available aliases in the session. 

Here, we’re using this call to see the objects that were created for our toy program and validate it corresponds to the ones we would expect. Everything looks good!

Now, for the big moment! lets run our walker on the root node of the graph we created and see what happens!

```
jaseci > walker run create_fam
I didn’t do any of the hard work.
[]
jaseci >

```

We see the standard output we’d expect from our toy program

But there were many semantics to what our toy program does. How do we visualize that the graph produced by or program is right. Well we’re in luck! We can use Jaseci `dot` features to take a look at our graph.

```
jaseci > graph get -mode dot -o fam.dot
strict digraph root {
    "n0" [ id="550ce1bb405c4477947e019d1e8428eb", label="n0:root" ]
"n1" [ id="e5c0a9b28f134313a28794a0c061bff1", label="n1:man" ]
"n2" [ id="bc2d2f18e2de4190a50bec2a32392a4f", label="n2:woman" ]
"n3" [ id="92ed7781c6674824905b149f7f320fcd", label="n3:man" ]
"n1" -> "n3" [ id="76535f6c3f0e4b7483c31863299e2784", label="e0:dad" ]
"n3" -> "n2" [ id="6bb83ee19f8b4f7eb93a11f5d4fa7f0a", label="e1:mom" ]
"n1" -> "n2" [ id="0fc3550e75f241ce8d1660860cf4e5c9", label="e2:married", dir="both" ]
"n0" -> "n2" [ id="03fcfb60667b4631b46ee589d982e1ce", label="e3" ]
"n0" -> "n1" [ id="d1713ac5792e4272b9b20917b0c3ec33", label="e4" ]
}
[saved to fam.dot]
jaseci >

```

Here we’ve used the `graph get` core API to get a print out of the graph in dot format. 

By default graph get dumps out a list of all edge and node objects of the graph, however with the `-mode dot` parameter we’ve specified that the graph should be printed in dot. 

The `-o` flag specifies a file to dump the output of the command. Note that the `-o` flag for jsctl commands only outputs the formal returned data (json payload, or string) from a Jaseci Core API. 
Logging output, standard output, etc will not be saved to the file though anything reported by a walker using report will be saved. This output file directive is `jsctl` specific and work with any command given to `jsctl`.

### Using **Graphviz** for visualizing

To see a pretty visual of the graph itself, we can use the dot command from Graphviz. Simply type:

```
dot -Tpdf fam.dot -o fam.pdf

```

We can see the beautiful graph our toy Jac program has produced on its way to the standard output.







