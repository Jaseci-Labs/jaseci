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

Please refer to [Key Abstractions and Concepts](../../category/abstractions-of-jaseci) for the key new concepts in a nutshell. These will make more sense as you go through this guide.

### Graph, nodes, edges

Refer to [Graphs](../../docs/development/abstractions/graphs) for more.

### Walkers

Refer to relevant sections. These will make more sense as you go through this guide.

- [Walkers](../../docs/development/abstractions/walkers)


### Abilities

Refer to relevant sections. These will make more sense as you go through this guide.

- [Abilities](../../docs/development/abstractions/abilities)
    - [`here` and `visitor`](../../docs/development/abstractions/abilities#here-and-visitor)

### Actions

Refer to relevant sections. These will make more sense as you go through this guide.

- [Actions](../../docs/development/abstractions/actions)
