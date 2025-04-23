import:py from jaclang.runtimelib.machine { JacMachine, JacMachineState }

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
    node_arch = JacMachine.create_architype_from_source(JacMachine.py_get_jac_machine(),
        dynamic_module_source,
        module_name="dynamic_module"
    );
    walker_obj = JacMachine.spawn_walker(JacMachine.py_get_jac_machine(),
        'DynamicWalker',
        module_name="dynamic_module",

    );
    root spawn walker_obj;
}
