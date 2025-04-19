import:py from jaclang.runtimelib.feature { JacFeature, JacMachineState }
# Dynamically create a node architype
glob source_code = """
node dynamic_node {
has value:int;
can print_value with entry {
print("Dynamic Node Value:", f'{self.value}');
}
}
""";

# Create a new walker architype dynamically
glob walker_code = """
walker dynamic_walker {
can visit_nodes with entry {
visit [-->];
}
}
""";

with entry {
    node_arch = JacFeature.create_architype_from_source(JacMachineState.get(), source_code);
    walker_arch = JacFeature.create_architype_from_source(JacMachineState.get(), walker_code);

    node_obj = JacFeature.spawn_node(JacMachineState.get(),
        'dynamic_node',
        {'value': 99},
        node_arch.__name__
    );
    walker_obj = JacFeature.spawn_walker(JacMachineState.get(),
        'dynamic_walker',
        module_name=walker_arch.__name__
    );
    node_obj spawn walker_obj;
}
