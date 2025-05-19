import from jaclang.runtimelib.machine { JacMachineInterface, JacMachine }

glob dynamic_module_source = """
import from .arch_create_util {UtilityNode}

walker DynamicWalker {
can start with entry {
print("DynamicWalker Started");
here ++> UtilityNode(data=42);
visit [-->](`?UtilityNode);
}

def UtilityNode {
here.display_data();
}
}
""";

with entry {
    node_arch = JacMachineInterface.create_archetype_from_source(JacMachineInterface.py_get_jac_machine(),
        dynamic_module_source,
        module_name="dynamic_module"
    );
    walker_obj = JacMachineInterface.spawn_walker(JacMachineInterface.py_get_jac_machine(),
        'DynamicWalker',
        module_name="dynamic_module",

    );
    root spawn walker_obj;
}
