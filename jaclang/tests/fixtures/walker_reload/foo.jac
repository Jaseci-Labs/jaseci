import:py from jaclang.plugin.feature { JacFeature as Jac }
import:jac from bar { bar_walk }
import:py from time { sleep }
import:py os;

can update_bar_walker {
    new_behavior = '''
    # New behavior added during runtime
    can end with `root exit {
    "bar_walk has been updated with new behavior!" |> print;
    disengage;
    }
    }
    ''';
    bar_file_path = os.path.abspath(
        'jaclang/tests/fixtures/walker_reload/bar.jac'
    );
    with open(bar_file_path, 'r') as bar_file {
        original_content = bar_file.read();
    }
    with open(bar_file_path, 'r+') as bar_file { # Specify the correct path to bar.jac

    content = bar_file.read();

    # Replace the last occurrence of "}" with the new behavior
    last_brace_index = content.rfind('}');
    if last_brace_index != -1 {
        updated_content = content[:last_brace_index] + new_behavior;
        bar_file.seek(0);
        bar_file.write(updated_content);
        bar_file.truncate();
    }
    }
    "Updated bar.jac with new behavior." |> print;
    (bar_walk_new, ) = Jac.context().jac_machine.update_walker(
        "bar",
        items={'bar_walk': None}
    );
    "Running bar_walk after update..." |> print;
    root spawn bar_walk_new();
    print(f"bar_walk: {bar_walk_new.__dict__}");
    with open(bar_file_path, 'w') as bar_file {
        bar_file.write(original_content);
    }
}
# Initialize the walker

can initial_run {
    root spawn bar_walk();
    print(f"bar_walk: {bar_walk.__dict__}");
}
# Define the entry point to run the test

with entry {
    initial_run();

    # Update the walker
    update_bar_walker();
}
