import:jac from .multi_import2 {A, create_node, B} # B is not existing

walker check_node {
    can enter with `root entry {
        visit [-->(`?A)];
    }

    can enter2 with A entry {
        print(here);
    }
}

