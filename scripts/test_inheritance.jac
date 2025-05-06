"""Test file for inheritance pattern conversion"""

# Single inheritance with obj
obj Circle(Shape) {
    def init(radius: float) {
        super.init();
        self.radius = radius;
    }
}

# Single inheritance with node
node UserProfile(Person) {
    has name: str;
    has age: int;
}

# Single inheritance with edge
edge Friendship(Relationship) {
    has strength: float;
}

# Single inheritance with walker
walker ProfileVisitor(Visitor) {
    def visit_entry {
        // do something
    }
}

# Multiple inheritance
obj MultiChild(Parent1, Parent2) {
    has feature: str;
}

# Make sure we don't break normal code
obj SimpleClass {
    has value: int;
}

# Additional test cases
node CompactNode(Base) {
    // No spaces in pattern
}

walker CompactWalker(Base) {
    // No spaces in pattern
}

obj    SpacyClass(BaseClass) {
    // Extra spaces in pattern
}