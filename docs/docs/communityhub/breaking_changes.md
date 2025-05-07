# Breaking Changes

This page documents significant breaking changes in Jac and Jaseci that may affect your existing code or workflows. Use this information to plan and execute updates to your applications.

## Latest Breaking Changes

### Version 0.8.0 (Main branch since 5/5/2025)

#### 1. `def` keyword introduced

Instead of using `can` keyword for all functions and abilities, `can` statements are only used for data spatial abilities and `def` keyword must be used for traditional python like functions and methods.

**Before (v0.7.x and earlier):**
```jac
node Person {
    has name;
    has age;

    can get_name {
        return self.name;
    }

    can greet with speak_to {
        return "Hello " + visitor.name + ", my name is " + self.name;
    }

    can calculate_birth_year {
        return 2025 - self.age;
    }
}
```

**After (v0.8.0+):**
```jac
node Person {
    has name;
    has age;

    def get_name {
        return self.name;
    }

    can greet with speak_to entry {
        return "Hello " + visitor.name + ", my name is " + self.name;
    }

    def calculate_birth_year {
        return 2025 - self.age;
    }
}
```

#### 2. `visitor` keyword introduced

Instead of using `here` keyword to represent the other object context while `self` is the self referencial context. Now `here` can only be used in walker abilities to reference a node or edge, and `visitor` must be used in nodes/edges to reference the walker context.

**Before (v0.7.x and earlier):**
```jac
node Person {
    has name;

    can greet {
        self.name = self.name.upper();
        return "Hello, I am " + self.name;
    }

    can update_walker_info {
        here.age = 25;  # 'here' refers to the walker
    }
}

walker PersonVisitor {
    has age;

    can visit: Person {
        here.name = "Visitor";  # 'here' refers to the current node
        report here.greet();
    }
}
```

**After (v0.8.0+):**
```jac
node Person {
    has name;

    can greet {
        self.name = self.name.upper();
        return "Hello, I am " + self.name;
    }

    can update_walker_info {
        visitor.age = 25;  # 'visitor' refers to the walker
    }
}

walker PersonVisitor {
    has age;

    can visit: Person {
        here.name = "Visitor";  # 'here' still refers to the current node in walker context
        report here.greet();
    }
}
```

This change makes the code more intuitive by clearly distinguishing between:
- `self`: The current object (node or edge) referring to itself
- `visitor`: The walker interacting with a node/edge
- `here`: Used only in walker abilities to reference the current node/edge being visited

#### 3. Changes to lambda syntax and `lambda` instroduced

Instead of using the `with x: int can x;` type syntax the updated lambda syntax now replaces `with` and `can` with `lambda` and `:` repsectively.

**Before (v0.7.x and earlier):**
```jac
# Lambda function syntax with 'with' and 'can'
with entry {
    square_func = with x: int can x * x;
}
```

**After (v0.8.0+):**
```jac
# Updated lambda
with entry {
    square_func = lambda x: int: x * x;
}
```

This change brings Jac's lambda syntax closer to Python's familiar `lambda parameter: expression` pattern, making it more intuitive for developers coming from Python backgrounds while maintaining Jac's type annotations.

#### 4. Data spatial arrow notation updated

The syntax for typed arrow notations are updated as `-:MyEdge:->` and `+:MyEdge:+>` is now `->:MyEdge:->` and `+>:MyEdge:+> for reference and creations.

**Before (v0.7.x):**
```jac
friends = [-:Friendship:->];
alice <+:Friendship:strength=0.9:+ bob;
```

**After (v0.8.0+):**
```jac
friends = [->:Friendship:->];
alice <+:Friendship:strength=0.9:<+ bob;
```

This change was made to eliminate syntax conflicts with Python-style list slicing operations (e.g., `my_list[:-1]` was forced to be written `my_list[: -1]`). The new arrow notation provides clearer directional indication while ensuring that data spatial operations don't conflict with the token parsing for common list operations.

#### 5. Import `from` syntax updated for clarity

The syntax for importing specific modules or components from a package has been updated to use curly braces for better readability and to align with modern language conventions.

**Before (v0.7.x):**
```jac
import from pygame_mock, color, display;
import from utils, helper, math_utils, string_formatter;
```

**After (v0.8.0+):**
```jac
import from pygame_mock { color, display };
import from utils { helper, math_utils, string_formatter };
```

This new syntax using curly braces makes it clearer which modules are being imported from which package, especially when importing multiple items from different packages.

