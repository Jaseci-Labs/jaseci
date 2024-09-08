---
sidebar_position: 2
description: An Overview of Walkers and Examples.
---

# Walkers

The concept of a walker is one of the new programming language abstractions introduced by Jaseci and the
Jack Language. In a nutshell, a walker is a unit of execution that retains state (its context scope, i.e.,
has variables) as it travels over a graphs. Walkers *walk* from node to node in the graph and executing its body.
The walker’s body is specified with an opening and closing braces ( `{` `}` ) and is executed to
completion on each node it lands on. In this sense a walker iterates while spooling through a
sequence of nodes that it ‘takes’ using the take keyword. We call each of these iterations
node-bound iterations.

Variables in a walker's body are divided into two categories: context variables, which retain their values as the walker moves through the graph, and local variables, which are reinitialized for each node-bound iteration.

> **Note**
>
> Walkers are initialized with default context variables on creation. Has variables only clear on destruction
and can be overwritten with calls to `walker_prime`. The intuition here is walkers simply keep state until they are destroyed.

Walkers offer a different approach to programmatic execution, distinct from the common function-based model used in other languages. Instead of a function's scope being temporarily pushed onto a growing stack as functions call other functions, scopes in Jaseci can be laid out spatially on the graph and walkers can traverse the graph, carrying their scope with them. This new model introduces data-spatial problem solving, where walkers can access any scope at any time in a modular manner, unlike in the function-based model where scopes become inaccessible after a function is called until it returns.

When solving problems with walkers, a developer can think of that walker as a little self-contained robot or agent that can retain context as it spatially moves about a graph, interacting with the context in nodes and edges of that graph.

## Init Walker with Examples

When we run a jac code, by default it's executing the `init` walker. Basically the `walker init` works as the main method in other programming language. save following code as `main.jac` and run the code in `jsctl` shell with `jac run main.jac`

```jac
walker init{
    std.out("This is from init walker \n");
}
```

Expected Output:

```
    This is from init walker
```
As you can see, this code has executed the `init` walker. Now let's create another walker;

```jac
walker second_walker{
    std.out("This is from second walker \n");
}

walker init{
    std.out("This is from init walker");
    root{
        spawn here walker::second_walker;
    }
}

```

Expected Output:
```
    This is from init walker
    This is from second walker
```

The statements from `second walker` and `init` are printed in the jac shell, and we may run just `second_walker` directly by using the command `jac run main.jac -walk second_walker`. Here, the `-walk` parameter instructs the `jsctl` to execute a certain walker.

## Walkers Navigating Graphs Examples

As mentioned earlier the walkers can traverse(walk) through the nodes of the graph in breadth first search (BFS) or depth first search(DFS) approaches.

> **Note**
>
> BFS is a traversal approach in which begins from root node and walk through all nodes on the same level before moving on to the next level. DFS is also a traversal approach in which the traverse begins at the root node and proceeds through the nodes as far as possible until we reach the node with no unvisited nearby nodes.

We are creating the following graph to demonstrate traversing of walkers in the coming sections;

 ![Example Graph - Navigating](img/traverse_graph_example.png)

Jaseci introduces the handy command called "take" to instruct walker to navigate through nodes. See how that works in following example;

```jac
node plain: has number;

## defining the graph
graph example {
    has anchor head;
    spawn {
        n=[];
        for i=0 to i<7 by i+=1 {
            n.l::append(spawn node::plain(number=i+1));
        }

        n[0] ++> n[1] ++> n[2];
        n[1] ++> n[3];
        n[0] ++> n[4] ++> n[5];
        n[4] ++> n[6];
        head=n[0];
        }
    }

#init walker traversing
walker init {
    root {
        start = spawn here ++> graph::example;
        take-->;
        }
    plain {
        std.out(here.number);
        take-->;
    }
}
```

Expected Output:

```
1
2
5
3
4
6
7
```

`take` command lets the walker traverse through graph nodes. You may notice by default, a walker traverse with `take` command using the breadth first search approach. But the `take` command is flexible hence you can indicate whether the take command should use a depth first or a breadth first traversal to navigate. Look at the following example; More information about `take` command and keywords to operate walkers can be found [here](../operations/take.md)

In addition to the introduction of the `take` command to support new types of control flow for node-bound iterations. The keywords and semantics of `disengage`, `skip`, and `ignore` are also introduced. These instruct walkers to stop walking the graph, skip over a node for execution, and ignore certain paths of the graph. More information about these can be found in [here](../operations/skip.md)

<!-- Is it necessary to have bfs,dfs traversals and skip, disengage traversals in the operators sections. I need feedback on this-->

## Walker Spawning Examples

Jaseci walkers act like little robots traversing graphs, with a unique ability to spawn other walkers that can also walk the graph and return a value to the parent walker. This powerful feature is achieved by specifying the variable to receive the returned value using the **`has anchor some_variable`** syntax.

Here's a simple example of how to use walker spawning in Jaseci:

```jac
walker parent {
    has result;

    result = spawn here walker::child;

    std.out("Child walker returned: ", result);
}

walker child {
    has anchor return_value;

    return_value = "Hello, I am the child walker!";
}
```

In this example, the parent walker spawns the child walker and sets the return_value anchor to a string. The parent walker then assigns its result variable to the value returned by the child walker, and finally outputs the returned value using std.out.

With this feature, you can easily create dynamic traversal patterns that adapt to changing data and requirements, making Jaseci a powerful tool for developing complex applications.

## Walker Callback

Walker callback is used for running a walker to a specific node using `public key` instead of authorization token.

### Use Case
Generating public URL that can be used as callback API for 3rd party Webhook API.
You may also use this as a public endpoint just to run a specific walker to a specific node.

### Structure

**POST** /js_public/walker_callback/`{node uuid}`/`{spawned walker uuid}`?key=`{public key}`

### Steps to Generate

**1. Jac Code**

```js
walker sample_walker: anyone {
    has fieldOne;
    with entry {
        report 1;
    }
}
```

**2. Register Sentinel**

```bash
curl --request POST \
  --url http://localhost:8000/js/sentinel_register \
  --header 'Authorization: token {yourToken}' \
  --header 'Content-Type: application/json' \
  --data '{ "name": "sentinel1", "code": "walker sample_walker: anyone {\r\n\thas fieldOne;\r\n\twith entry {\r\n\t\treport 1;\r\n\t}\r\n}" }'
```
```json
// RESPONSE
[
	{
		"version": "3.5.7",
		"name": "zsb",
		"kind": "generic",
		"jid": "urn:uuid:b4786c7a-cf24-49a4-8c2c-755c75a35043",
		"j_timestamp": "2022-05-11T05:57:07.849673",
		"j_type": "sentinel"
	}
]
```

**3. Spawn Public Walker** (sample_walker)

```bash
curl --request POST \
  --url http://localhost:8000/js/walker_spawn_create \
  --header 'Authorization: token {yourToken}' \
  --header 'Content-Type: application/json' \
  --data '{ "name": "sample_walker", "snt":"active:sentinel" }'
```
```json
// RESPONSE
{
	"context": {},
	"anchor": null,
	"name": "sample_walker",
	"kind": "walker",
	// this is the spawned walker uuid to be used
	"jid": "urn:uuid:2cf6d0dc-e7eb-4fc8-8564-1bbdb48baad3",
	"j_timestamp": "2022-06-07T09:45:22.101017",
	"j_type": "walker"
}
```

**4. Getting Public Key**

```bash
curl --request POST \
  --url http://localhost:8000/js/walker_get \
  --header 'Authorization: token {yourToken}' \
  --header 'Content-Type: application/json' \
  --data '{ "mode": "keys", "wlk": "spawned:walker:sample_walker", "detailed": false }'
```
```json
// RESPONSE
{
	// this is the public key used for walker callback
	"anyone": "97ca941e6bf1f43c3a4e531e40b2ad5a"
}
```

**5. Construct the URL**
*Assuming there's a node with uuid of `aa1bb26e-238b-40a0-8e39-333ec363ace7`*
*this endpoint can now be accessible by anyone*

>**POST** /js_public/walker_callback/`aa1bb26e-238b-40a0-8e39-333ec363ace7`/`2cf6d0dc-e7eb-4fc8-8564-1bbdb48baad3`?key=`97ca941e6bf1f43c3a4e531e40b2ad5a`