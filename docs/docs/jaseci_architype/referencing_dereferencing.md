# Referencing and Dereferencing Nodes

In Jaseci language, referencing and dereferencing of nodes and edges are similar to the references in many programming languages, and they adopt the syntax of pointers in C/C++. The symbol & is used to retrieve the reference of an object, while the symbol * is used for dereferencing. Unlike C/C++, Jaseci references use a unique identifier in UUID format instead of memory locations.

When an object is dereferenced, it is represented as a string in UUID format that corresponds to the unique identifier of the object. This UUID is equivalent to the jid in the object's .info. These referencing and dereferencing operations are useful for input and output of node locations to the client-side, among other applications.

It is important to note that an instance of an archetype is internally represented as a string composed of a UUID that starts with "jac:uuid:". Although this may change in the future, if you assign such a string to a variable in a Jaseci program, the program will treat it like an object.

```jac
node simple: has name;

 walker ref_deref {
    with entry {
        for i=0 to i<3 by i+=1:
        spawn here ++> node::simple(name="node"+i.str);
    }
    var = &(++>[0]);
    std.out('ref:', var);
    std.out('obj:', *var);
    std.out('info:',(*var).info);
}
```
**Output**
```
ref: urn:uuid:04295f7f-a5bf-4db3-87ce-e13653a81b25
obj: jac:uuid:04295f7f-a5bf-4db3-87ce-e13653a81b25
info: {
    "context": {
        "name": "node0"
        }, 
    "anchor": null, 
    "name": "simple", 
    "kind": "node", 
    "jid": "urn:uuid:04295f7f-a5bf-4db3-87ce-e13653a81b25", 
    "j_timestamp": "2022-08-10T15:57:00.577287", 
    "j_type": "node"
}
```

The code snippet creates a simple node with an attribute named name. It then initializes a walker named ref_deref, which creates three new nodes named node0, node1, and node2 and assigns them to the simple node.

The code then assigns the reference of the first node node0 to the var variable using the & operator. The std.out() function is used to print out the reference, object, and information related to the var variable.

When executed, the code will output the reference and information related to the node0 object. The obj output shows the UUID of the node0 object, while the info output shows the complete information related to the simple node, including its context, anchor, name, kind, and other attributes.