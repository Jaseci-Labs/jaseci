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
    node_arch = __jac_mach__.create_architype_from_source(source_code);
    walker_arch = __jac_mach__.create_architype_from_source(walker_code);

    node_obj = __jac_mach__.spawn_node(
        'dynamic_node',
        {'value': 99},
        node_arch.__name__
    );
    walker_obj = __jac_mach__.spawn_walker(
        'dynamic_walker',
        module_name=walker_arch.__name__
    );
    node_obj spawn walker_obj;
}
