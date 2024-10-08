import from .arch_create_util {UtilityNode}

walker DynamicWalker {
can start with entry {
print("DynamicWalker Started");
here ++> UtilityNode(data=42);
visit [-->](`?UtilityNode);
}

can UtilityNode {
here.display_data();
}
}

with entry {
    root spawn DynamicWalker();
}