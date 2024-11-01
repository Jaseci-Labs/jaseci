import:py from jaclang.runtimelib.machine { JacMachine }

glob dynamic_module_source = """
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
""";

with entry {
    node_arch = JacMachine.get().create_architype_from_source(
        dynamic_module_source,
        module_name="dynamic_module"
    );
    walker_obj = JacMachine.get().spawn_walker(
        'DynamicWalker',
        module_name="dynamic_module",

    );
    root spawn walker_obj;
}
