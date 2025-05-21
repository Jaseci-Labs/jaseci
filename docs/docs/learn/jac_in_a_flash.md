# <span style="color: orange; font-weight: bold">Jac in a Flash</span>

This mini tutorial uses a single toy program to highlight the major pieces of
the Jac language.  We start with a small Python game and gradually evolve it
into a fully data‑spatial Jac implementation.  Each iteration introduces a new
Jac feature while keeping the overall behaviour identical.

## Step&nbsp;0 – The Python version

Our starting point is a regular Python program that implements a simple "guess
the number" game.  The player has several attempts to guess a randomly generated
number.

=== "guess_game.py"
    ```jac linenums="1"
    --8<-- "jac/examples/guess_game/guess_game.py"
    ```

## Step&nbsp;1 – A direct Jac translation

`guess_game1.jac` mirrors the Python code almost line for line.  Classes are
declared with `obj` and methods with `def`.  Statements end with a semicolon and
the parent initializer is invoked via `super.init`.  Program execution happens
inside a `with entry { ... }` block, which replaces Python's
`if __name__ == "__main__":` section.  This step shows how familiar Python
concepts map directly to Jac syntax.

=== "guess_game1.jac"
    ```jac linenums="1"
    --8<-- "jac/examples/guess_game/guess_game1.jac"
    ```

## Step&nbsp;2 – Declaring fields with `has`

The second version moves attribute definitions into the class body using the
`has` keyword.  Fields may specify types and default values directly on the
declaration.  Methods that take no parameters omit parentheses in their
signature, making the object definition concise.

=== "guess_game2.jac"
    ```jac linenums="1"
    --8<-- "jac/examples/guess_game/guess_game2.jac"
    ```

## Step&nbsp;3 – Introducing the pipe operator

`guess_game3.jac` demonstrates Jac's pipe forward operator (`|>`).  It pipes the
result of the expression on the left as arguments to the function on the right.
Calls like `print("hi")` become `"hi" |> print` and expressions can be chained
(`guess |> int |> self.process_guess`).  The pipe is also used for object
construction and method invocation (`|> GuessTheNumberGame`).

=== "guess_game3.jac"
    ```jac linenums="1"
    --8<-- "jac/examples/guess_game/guess_game3.jac"
    ```

## Step&nbsp;4 – Separating implementation with `impl`

The fourth version splits object declarations from their implementations using
`impl`.  The object lists method signatures (`def init;`, `override def play;`),
and the actual bodies are provided later in `impl Class.method` blocks.  This
separation keeps the interface clean and helps organise larger codebases.

=== "guess_game4.jac"
    ```jac linenums="1"
    --8<-- "jac/examples/guess_game/guess_game4.jac"
    ```
=== "guess_game4.impl.jac"
    ```jac linenums="1"
    --8<-- "jac/examples/guess_game/guess_game4.impl.jac"
    ```

## Step&nbsp;5 – Walking the graph

Finally `guess_game5.jac` re‑imagines the game using Jac's data‑spatial
architecture.  A `walker` visits a chain of `turn` nodes created with `++>`
edges.  The walker moves with `visit [-->]` and stops via `disengage` when the
guess is correct.  The game is launched by `spawn`ing the walker at `root`.
This example shows how conventional logic can become graph traversal.

=== "guess_game5.jac"
    ```jac linenums="1"
    --8<-- "jac/examples/guess_game/guess_game5.jac"
    ```
=== "guess_game5.impl.jac"
    ```jac linenums="1"
    --8<-- "jac/examples/guess_game/guess_game5.impl.jac"
    ```

Happy code deconstructing!
