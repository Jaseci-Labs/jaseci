# Preparation
Jaseci requires python3.10 or higher as well as a set of common dependencies. If you are on a fresh linux environment, make sure to install the following first:

```
apt-get install python3.10-dev python3-pip git g++ build-essential pkg-config cmake
```

To install jaseci, run this in your development environment:

```
pip install jaseci
```

To test the installation is successful, run:

```
jsctl --help
```

`jsctl` stands for the Jaseci Command Line Interface.
If the command above displays the help menu for `jsctl`, then you have successfully installed jaseci.

> **Note**
>
> Take a look and get familiarized with these commands while you are at it. `jsctl` will be frequently used throughout this journey.

The following sections will require training files from the Jaseci repository:

`https://github.com/Jaseci-Labs/jaseci`

After forking the repository, the files can be found in `examples/CanoniCAI/code`

## Key Concepts

Please refer to [Key Abstractions and Concepts](lang_docs/key_concepts.md) for the key new concepts in a nutshell. These will make more sense as you go through this guide.

### Graph, nodes, edges

Refer to [Graphs](lang_docs/graphs.md) for more.

### Walkers

Refer to relevant sections. These will make more sense as you go through this guide.

- [Walkers](lang_docs/walkers.md)
- [Walkers By Example](lang_docs/walkers_by_example.md)

### Abilities

Refer to relevant sections. These will make more sense as you go through this guide.

- [Abilities](lang_docs/abilities.md)
    - [`here` and `visitor`](lang_docs/here_visitor.md)
- [Abilities By Example](lang_docs/abilities_by_example.md)

### Actions

Refer to relevant sections. These will make more sense as you go through this guide.

- [Actions](lang_docs/actions.md)
- [Actions By Example](lang_docs/actions_by_example.md)