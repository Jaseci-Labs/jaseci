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
    node_arch = JacFeature.create_architype_from_source(JacFeature.py_get_jac_machine(), source_code);
    walker_arch = JacFeature.create_architype_from_source(JacFeature.py_get_jac_machine(), walker_code);

    node_obj = JacFeature.spawn_node(JacFeature.py_get_jac_machine(),
        'dynamic_node',
        {'value': 99},
        node_arch.__name__
    );
    walker_obj = JacFeature.spawn_walker(JacFeature.py_get_jac_machine(),
        'dynamic_walker',
        module_name=walker_arch.__name__
    );
    node_obj spawn walker_obj;
}
