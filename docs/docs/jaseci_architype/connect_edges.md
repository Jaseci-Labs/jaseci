# Connect Operator

In Jaseci, operators are used to connect nodes and form graphs. The operators available for connecting nodes are:

1. ++> : This operator is used to connect two nodes in a forward direction. For example, node1 ++> node2 will connect node1 to node2.
2. <++> : This operator is used to connect two nodes in a backward direction. For example, node2 <++> node1 will connect node2 to node1.
3. <+[name_of_edge]+> : This operator is used to connect two nodes in a backward direction with a custom edge type. For example, node2 <+[custom_edge]+> node1 will connect node2 to node1 with a custom edge type named custom_edge.
4. +[name_of_edge]+> : This operator is used to connect two nodes in a forward direction with a custom edge type. For example, node1 +[custom_edge]+> node2 will connect node1 to node2 with a custom edge type named custom_edge.
5. <+[name_of_edge(variable_declared = some_value)]+> : This operator is used to connect two nodes in a backward direction with a custom edge type that has a variable declared with a specific value. For example, node2 <+[custom_edge(my_var = 42)]+> node1 will connect node2 to node1 with a custom edge type named custom_edge and a variable my_var declared with the value 42.
6. +[name_of_edge(variable_declared = some_value)]+> : This operator is used to connect two nodes in a forward direction with a custom edge type that has a variable declared with a specific value. For example, node1 +[custom_edge(my_var = "hello")]+> node2 will connect node1 to node2 with a custom edge type named custom_edge and a variable my_var declared with the value "hello".

These operators allow you to create complex graphs with customized edge types that can hold specific values. By using these operators, you can create a network of nodes that can represent complex data structures, such as trees or graphs. The use of customized edge types also allows you to define specific behavior for different types of connections between nodes.