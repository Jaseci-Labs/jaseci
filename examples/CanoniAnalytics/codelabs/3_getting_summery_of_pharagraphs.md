# Retriving Summery Of Text

We created a graph from the movie script data in the previous part. You may have noticed that some movie scene descriptions are rather lengthy and take a while to read. How simple it would be if we could summarize that lengthy phaseges. Yes, that is what we will accomplish in this section.

For this section we are using jaseci NLP features. To get summeries Jaseci has several modules already implemented, but here for demostration purpose we will be using the `jac_nlp.bart_sum` the **BART summerizer**. For all other available Jaseci summerization modules refer to [here](../../../README.md)

### 1. Installing Jac NLP summerization module

Before get started you have to install `jac_nlp.bart_sum` using the following command.

```
pip install jac_nlp[bart_sum]
```

### 2. Updating the scene node to set summery of descriptions

In this section we are going to modify the code which we were used in previous section. You may notices in the previous section the scene node had only two variables `name` and `description`. Since here we are going to extract description summery we are creating another variable in scene node to store the scene description. see the modification we have done to the `scene node`.

```jac
node scene{
    has name;
    has description;
    has desc_summery;

    can set_summery with summerizer entry{
        here.desc_summery = visitor.summery;
    }
}
```

Also we have added Jaseci `ability` here. to know more about jaseci abilities go to [here](../canoniCAI/codelab/lang_dogs/../../../../CanoniCAI/codelabs/lang_docs/abilities.md) and for examples about abilities [here](../canoniCAI/codelabs/../../../CanoniCAI/codelabs/lang_docs/abilities_by_example.md).


### 3. Creating the summerizer walker.

Now lets going to create the summerizer walker.

```
walker summerizer {
    can bart_sum.summarize;
    has text;
    has summery;

    summery = bart_sum.summarize(text, 20);
}
```

- `can bart_sum.summerize` this is the action we are using to summerize text features.
-  in `summery = bart_sum.summarize(text, 20)` line we are calling the jaseci bart_sum.summerze action. the `text` variable has declared by yet not assigned a value to. We are going to get that value from the `scene node`.


### 4. Wrapping things up with the init walker

Now lets connect all together with the `init` walker.

```
walker init{
    root{
         spawn here walker::build_graph;
         take-->;
    }

    scene{
        spawn here walker::summerizer(text=here.description);
        take -->node::scene;
    }
}
```

- `spawn here walker::build_graph` spawining the graph from the root node.
- `take-->` travers starts from the root node.
- `spawn here walker::summerizer(text=here.description);` This line is the most important part in this code. This creates the summery using the summerize walker. `here.description` is to get the description from the current `scene` node.
- `take -->node::scene;` thie take keyworrd command walkers to travers around the graph. here the speciallity is this command says walkers to travers only in `scene` nodes. For more details about traversings of walkers please refer to [here](../canoniCAI/codelabs/lang_docs/../../../../CanoniCAI/codelabs/lang_docs/walkers_by_example.md).


Save all these changes and load the `bart_sum` module before run the code in `jsctl` terminal.

```
actions load module jac_nlp.bart_sum
jac run movie.jac
```
If everything is fine you will see a output similar to this.

```
jaseci > jac run movie.jac
{
  "success": true,
  "report": [],
  "final_node": "urn:uuid:1c75b708-06ed-45a8-a2ee-88a94a3c33da",
  "yielded": false
}
```

To be amazed by the graph view and the read the summeries you have to register the updated code in the jaseci server.

Steps to re-launch the new program in Jaseci Studio;

**Step 1:** Build the jac file
```
jac build movie.jac
```

**Step 2:** Sentinel register the `jir`   file.
```
sentinel register movie.jir -set_active true -mode ir
```

**Step 3:** Get the sentinel ID (`jid`)

```
sentinel get
```

or

```
sentinel list
```

**Step 3:** Sentinel Set

```
sentinel set -snt JID -mode ir movie.jir
```

**Step 4:** Start and login to the server

**Step 5:** sentinel register in server

**Step 5:** Start the Jaseci Studio and view the graph