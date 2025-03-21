

can walk;

with entry{
    print('second.jac');
    print(walk());
}
can nested_import_func{

    import from global_import_from {display_from, Y};
    print(display_from(), Y);
}