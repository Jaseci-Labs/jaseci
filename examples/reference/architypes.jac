can print_base_classes(cls: type) -> type {
    print(f"Base classes of {cls.__name__}: {[c.__name__  for c in cls.__bases__]}");
    return cls;
}

obj Animal {}

obj Domesticated {}

@print_base_classes
node Mammal :Animal, Domesticated: {}

walker Dog :Mammal: {}

walker Labrador :Dog: {}

@print_base_classes
walker DecoratedLabrador :Labrador: {}
