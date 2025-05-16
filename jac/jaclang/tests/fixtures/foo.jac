import from jaclang.runtimelib.machine { JacMachineInterface, JacMachine }
import from bar { bar_walk }
# Test runner to initialize the walker

def test_run {
    # Print the loaded modules
    modules = JacMachineInterface.list_modules(JacMachineInterface.py_get_jac_machine());
    "Loaded Modules:" |> print;
    for mod_name in modules {
        f"Module: {mod_name}" |> print;
    }
    # Print walkers
    walkers = JacMachineInterface.list_walkers(JacMachineInterface.py_get_jac_machine(), mod_name);
    if walkers {
        f"Walkers in {mod_name}:" |> print;
        for walker in walkers {
            f"  - Walker: {walker}" |> print;
        }
    }
    # Print nodes
    nodes = JacMachineInterface.list_nodes(JacMachineInterface.py_get_jac_machine(), mod_name);
    if nodes {
        f"Nodes in {mod_name}:" |> print;
        for node in nodes {
            f"  - Node: {node}" |> print;
        }
    }
    # Print edges
    edges = JacMachineInterface.list_edges(JacMachineInterface.py_get_jac_machine(), mod_name);
    if edges {
        f"Edges in {mod_name}:" |> print;
        for edge in edges {
            f"  - Edge: {edge}" |> print;
        }
    }
    root spawn bar_walk();
}
# Define the entry point to run the test

with entry {
    test_run();
}
