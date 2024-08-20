import:py from jaclang.plugin.feature, JacFeature as Jac;
import:jac from bar, bar_walk;
import:py from time,sleep;



# Test runner to initialize the walker
can test_run {
    # Print the loaded modules
    modules = Jac.context().jac_machine.list_modules();
    "Loaded Modules:" |> print;
    for mod_name in modules {
        f"Module: {mod_name}" |> print;
    }
    # Print walkers
    walkers = Jac.context().jac_machine.list_walkers(mod_name);
        if walkers{
            f"Walkers in {mod_name}:" |> print;
            for walker in walkers{
                f"  - Walker: {walker}" |> print;
            }
        }

    # Print nodes
    nodes = Jac.context().jac_machine.list_nodes(mod_name);
    if nodes{
        f"Nodes in {mod_name}:" |> print;
        for node in nodes{
            f"  - Node: {node}" |> print;
        }
    }
    # Print edges
    edges = Jac.context().jac_machine.list_edges(mod_name);
    if edges{
        f"Edges in {mod_name}:" |> print;
        for edge in edges{
            f"  - Edge: {edge}" |> print;
        }
    }
    print(f"bar_walk: {bar_walk}");
    root spawn bar_walk();

    # Sleep to observe the update process
    "Sleeping for 5 seconds after update..." |> print;
    sleep(8);

    # Update the module
    (print_walk,)=Jac.context().jac_machine.update_module("bar", items={'print_walk': None});
    print(f"print_walk: {print_walk}");
    # Run the walker again after update
    "Running bar_walk after update..." |> print;
    root spawn print_walk();
}
# Define the entry point to run the test
with entry {
    test_run();
}
