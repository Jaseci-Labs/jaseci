<h1 style="color: orange; font-weight: bold; text-align: center;">Tour to Jac</h1>

## Python Superset Phylosophy: All of Python Plus More

Jac is a drop-in replacement for Python and supersets Python, much like Typescript supersets Javascript or C++ supersets C. It extends Python's semantics while maintaining full interoperability with the Python ecosystem, introducing cutting-edge abstractions designed to minimize complexity and embrace AI-forward development.

```jac
import math;
import from random { uniform }

def calculate_distance(x1: float, y1: float, x2: float, y2: float) -> float {
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2);
}

with entry {
    # Generate random points
    (x1, y1) = (uniform(0, 10), uniform(0, 10));
    (x2, y2) = (uniform(0, 10), uniform(0, 10));

    distance = calculate_distance(x1, y1, x2, y2);
    area = math.pi * (distance / 2) ** 2;

    print(f"Distance: {distance:.2f}, Circle area: {area:.2f}");
}
```
This snippet natively imports python packages `math` and `random` and runs identically to its Python counterpart. Jac targets python bytecode, so all python libraries work with Jac.


## Beyond OOP with Data Spatial Programming

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
    tour() spawn start;
}
```
A walker moves between nodes using edges, demonstrating Data Spatial Programming.


## Programming Abstractions for AI

Jac provides novel constructs for integrating LLMs into code. A function body can simply be replaced with a call to an LLM, removing the need for prompt engineering or extensive new libraries.

```jac
enum Personality {
    INTROVERT,
    EXTROVERT,
    AMBIVERT
}

can get_personality(name: str) -> Personality by llm();

with entry {
    result = get_personality("Albert Einstein");
    print(f"{result} personality detected");
}
```
`by llm()` delegates execution to an LLM without any extra library code.


## Zero to Infinite Scale with no Code Changes

Jac's cloud-native abstractions make persistence and user concepts part of the language so that simple programs can run unchanged locally or in the cloud. Deployments can be scaled by increasing replicas of the `jac-cloud` service when needed.

```jac
node Post { has content: str, author: str; }

walker create_post {
    has content: str, author: str;

    can with root entry {
        new_post = Post(content=self.content, author=self.author);
        here ++> new_post;
        report {"id": new_post.id, "status": "posted"};
    }
}
```
This simple social media post system runs locally or scales infinitely in the cloud with no code changes.


## Better Organized and Well Typed Codebases

Jac focuses on type safety and readability. Type hints are required and the built-in typing system eliminates boilerplate imports. Code structure can be split across multiple files, allowing definitions and implementations to be organized separately while still being checked by Jac's native type system.

=== "tweet.jac"

    ```jac
    obj Tweet {
        has content: str, author: str, likes: int = 0, timestamp: str;

        def like() -> None;
        def unlike() -> None;
        def get_preview(max_length: int) -> str;
        def get_like_count() -> int;
    }
    ```

=== "tweet.impl.jac"

    ```jac
    impl Tweet.like() -> None {
        self.likes += 1;
    }

    impl Tweet.unlike() -> None {
        if self.likes > 0 {
            self.likes -= 1;
        }
    }

    impl Tweet.get_preview(max_length: int) -> str {
        return self.content[:max_length] + "..." if len(self.content) > max_length else self.content;
    }

    impl Tweet.get_like_count() -> int {
        return self.likes;
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

