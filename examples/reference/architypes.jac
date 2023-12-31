
obj Animal {}

obj Domesticated {}

node Mammal:Animal,Domesticated: {}

walker Dog:Mammal: {}

walker Labrador:Dog: {}

can print_hierarchy(cls: type) {
    bases = list(cls.__bases__);
    for base in bases {
        bases.extend(print_hierarchy(base));
    }
    return bases;
}


can print_base_classes(cls: type) {
        hierarchy = print_hierarchy(cls);
        unique_hierarchy = {h.__name__ for h in hierarchy};
        print(
            f"Classes in the hierarchy of {cls.__name__}: {', '.join(unique_hierarchy)}"
        );
        return cls;
}

# Applying the decorator to the last class
@print_base_classes
walker DecoratedLabrador:Labrador: {}


with entry {
    # Example of using the decorated class
    decorated_labrador = (
        DecoratedLabrador()
    );  # This prints the base classes of DecoratedLabrador
    print(decorated_labrador._jac_);
}