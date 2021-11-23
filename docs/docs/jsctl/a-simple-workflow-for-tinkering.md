---
sidebar_position: 3
---

# A simple workflow for Tinkering

As you get to know Jaseci and Jac, you’ll want to try things and tinker a bit. 

In this section, we’ll get to know how `jsctl` can be used as the main platform for this play. 

A typical flow will involve jumping into shell-mode, writing some code, running that code to observe output, and in visualizing the state of the graph, and rendering that graph in dot to see it’s visualization.

### Heads up!

#### Install Graphvis

Before we jump right in, let me strongly encourage you install Graphviz. Graphviz is open source graph visualization software package that includes a handy dandy command line tool call dot. 

**Dot** is also a standardized and open graph description language that is a key primitive of Graphviz. 
The dot tool in Graphviz takes dot code and renders it nicely. 

Graphviz is super easy to install. 

##### Ubuntu
```
sudo apt install graphviz
```

MacOS
```
brew install graphviz
```

and you’re done! You should be able to call dot from the command line.

### Writing a simple Jac program

