Archetypes represent Jac's extension of traditional object-oriented programming classes, providing specialized constructs that enable data spatial programming. Each archetype type serves a distinct role in building topological computational systems where data and computation are distributed across graph structures.

#### Archetype Types

Jac defines four primary archetype categories that form the foundation of data spatial programming:

**Object (`obj`)**: Standard object archetypes that provide traditional class functionality with properties and methods. Objects serve as the base type from which all other archetypes inherit, ensuring compatibility with conventional programming patterns.

**Node (`node`)**: Specialized archetypes that represent discrete locations within topological structures. Nodes can store data, host computational abilities, and connect to other nodes through edges, forming the spatial foundation for graph-based computation.

**Walker (`walker`)**: Mobile computational entities that traverse node-edge structures, carrying algorithmic behaviors and state throughout the topological space. Walkers embody the "computation moving to data" paradigm central to data spatial programming.

**Edge (`edge`)**: First-class relationship archetypes that connect nodes while providing their own computational capabilities. Edges represent both connectivity and transition-specific behaviors within the graph structure.

#### Inheritance and Composition

Archetypes support multiple inheritance, enabling complex type hierarchies that reflect real-world relationships:

```jac
obj Animal;
obj Domesticated;

node Pet(Animal, Domesticated) {
    has name: str;
    has species: str;
}

walker Caretaker(Person) {
    can feed with Pet entry {
        print(f"Feeding {here.name} the {here.species}");
    }
}
```

The inheritance syntax `(ParentType1, ParentType2)` allows archetypes to combine behaviors from multiple sources, supporting rich compositional patterns.

#### Decorators and Metaprogramming

Decorators provide metaprogramming capabilities that enhance archetype behavior without modifying core definitions:

```jac
@print_base_classes
node EnhancedPet(Animal, Domesticated) {
    has enhanced_features: list;
}

@performance_monitor
walker OptimizedProcessor {
    can process with entry {
        # Processing logic with automatic performance tracking
        analyze_data(here.data);
    }
}
```

Decorators enable cross-cutting concerns like logging, performance monitoring, and validation to be applied declaratively across archetype definitions.

#### Access Control

Archetypes support access modifiers that control visibility and encapsulation:

```jac
node :pub DataNode {
    has :priv internal_state: dict;
    has :pub public_data: any;
    
    can :protect process_internal with visitor entry {
        # Protected processing method
        self.internal_state.update(visitor.get_updates());
    }
}
```

Access modifiers (`:pub`, `:priv`, `:protect`) enable proper encapsulation while supporting the collaborative nature of data spatial computation.

#### Data Spatial Integration

Archetypes work together to create complete data spatial systems:

```jac
node DataSource {
    has data: list;
    
    can provide_data with walker entry {
        visitor.receive_data(self.data);
    }
}

edge DataFlow(DataSource, DataProcessor) {
    can transfer with walker entry {
        # Edge-specific transfer logic
        transformed_data = self.transform(visitor.data);
        visitor.update_data(transformed_data);
    }
}

walker DataCollector {
    has collected: list = [];
    
    can collect with DataSource entry {
        here.provide_data();
        visit [-->];  # Continue to connected nodes
    }
}
```

This integration enables sophisticated graph-based algorithms where computation flows naturally through topological structures, with each archetype type contributing its specialized capabilities to the overall system behavior.

Archetypes provide the foundational abstractions that make data spatial programming both expressive and maintainable, enabling developers to model complex systems as interconnected computational topologies.
