<h1 style="color: orange; font-weight: bold; text-align: center;">Tour to Jac</h1>

# All of Python Plus More Phylosophy
Jac is a drop-in replacement for Python and supersets Python, much like Typescript supersets Javascript or C++ supersets C. It extends Python's semantics while maintaining full interoperability with the Python ecosystem, introducing cutting-edge abstractions designed to minimize complexity and embrace AI-forward development.

```jac
def add(x: int, y: int) -> int {
    return x + y;
}

with entry {
    print(add(2, 3));
}
```
This snippet runs identically to its Python counterpart, illustrating Jac's compatibility.


# Beyond OOP with Data Spatial Programming
Data Spatial Programming (DSP) inverts the traditional relationship between data and computation. Rather than moving data to computation, DSP moves computation to data through topologically aware constructs. This paradigm introduces specialized archetypes—objects, nodes, edges and walkers—that model spatial relationships directly in the language and enable optimizations around data locality and distributed execution.

```jac
node Place { has name: str; }

walker tour {
    can at Place entry {
        print("Visiting " + here.name);
        visit [-->];
    }
}

with entry {
    start = Place(name="Home");
    end = Place(name="Work");
    start ++> end;
    :> tour spawn start;
}
```
A walker moves between nodes using edges, demonstrating Data Spatial Programming.


# Programming Abstractions for AI
Jac provides novel constructs for integrating LLMs into code. A function body can simply be replaced with a call to an LLM, removing the need for prompt engineering or extensive new libraries.

```jac
can summarize(text: str) -> str by llm();

with entry {
    print(summarize("Jac simplifies LLM integration."));
}
```
`by llm()` delegates execution to an LLM without any extra library code.


# Zero to Infinite Scale with no Code Changes
Jac's cloud-native abstractions make persistence and user concepts part of the language so that simple programs can run unchanged locally or in the cloud. Deployments can be scaled by increasing replicas of the `jac-cloud` service when needed.

```jac
walker ping {
    can handle with root entry {
        report {"status": "ok"};
    }
}
```
Deployed with `jac-cloud`, this walker becomes a scalable REST endpoint.


# Better Organized and Well Typed Codebases
Jac focuses on type safety and readability. Type hints are required and the built-in typing system eliminates boilerplate imports. Code structure can be split across multiple files, allowing definitions and implementations to be organized separately while still being checked by Jac's native type system.

```jac
walker Greeter {
    def hello(name: str) -> None;
}
```
```jac
impl Greeter.hello(name: str) {
    print("Hello, " + name);
}
```
This shows how declarations and implementations can live in separate files for maintainable, typed codebases.

<div class="grid cards" markdown>

-   __In The Works__

    ---

    *Roadmap Items*

    [In The Roadmap](bigfeatures.md){ .md-button .md-button--primary }

-   __In The Future__

    ---

    *Research in Jac/Jaseci*


    [In Research](research.md){ .md-button }


</div>

