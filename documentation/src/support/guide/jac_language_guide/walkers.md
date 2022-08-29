# Walkers



* Walkers traverse nodes triggering execution at the node level.

* Walkers have the ability to pick upand retain context, which can be taken across nodes.

* Walkers also decides which node to travel to through next and records the path of travel to b recorded within it's own context.

* Walkers can be spawned at any node

* Walker can spawn other walkers.

* Walkers can carry with them their own actions and contexts that is executed whenever specified in the walkers own code



## Defining a Walker



```jac 

 walker [name_of_walker]{



}

```

Defining specific node code to execute When defining a walker, you also write specific code blocks that will only execute when the walker is on a specific node.



```jac

 walker [name_of_walker]{

    [Any code here is executed regardless of the node the walker is on]

    ...

    ...



    person{

     [Any code within this block will only be executed when the walker is on a person node]

   }



   ...



   family{

    [Any code within this block will only be executed when the walker is on a family node]

   }



}

```



## More on Behaivour with Abilities 



### With Entry and Exit 



When defining a walker, you also have the ability to write specific code blocks that execute if and only if a walker enters or exists a node. Any code within the with_entry block is the first thing that executes as soon as a walker enter a node. And the opposite is true for with_exit, triggering only when the walker is about to leave a node.



```jac 

walker [name_of_walker]{

    with entry{

        [code to execute when a walker first enters a node]

    }

    ...

    ...



    with exit{

        [code to execute when a walker is about to leave a node]

    }

}



```

