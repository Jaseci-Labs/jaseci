can print_base_classes(cls: type) -> type {
    print(f"Base classes of {cls.__name__}: {[c.__name__  for c in cls.__bases__]}");
    return cls;
}

obj Animal {}

obj Domesticated {}

@print_base_classes
obj Pet :Animal, Domesticated: {}

obj Person :Animal: {}

obj Feeder :Person: {}

@print_base_classes
obj Zoologist :Feeder: {}
