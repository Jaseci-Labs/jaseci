import:py from jaclang.runtimelib.feature { JacFeature, JacMachineState }

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
    node_arch = JacFeature.create_architype_from_source(JacMachineState.get(),
        dynamic_module_source,
        module_name="dynamic_module"
    );
    walker_obj = JacFeature.spawn_walker(JacMachineState.get(),
        'DynamicWalker',
        module_name="dynamic_module",

    );
    root spawn walker_obj;
}
