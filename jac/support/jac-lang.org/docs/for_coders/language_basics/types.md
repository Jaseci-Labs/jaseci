# Types and Type Hinting

## Primitive Types
Jac supports all Python primitive types including `int`, `float`, `str`, `bool`, `list`, `dict`, `set`, and `tuple`. These types work identically to their Python counterparts.

```jac linenums="1"
"""Demonstrates various primitive type usage"""
can process_data(id: int) -> dict{
    # Integer and float
    count: int = 42;
    price: float = 19.99;
    
    # String and boolean
    name: str = "item";
    active: bool = True;
    
    # List and set
    items: list = [1, 2, 3];
    unique_tags: set = {"red", "blue"};
    
    # Tuple and dictionary
    coords: tuple = (10, 20);
    details: dict = {"id": id, "name": name, "price": price, 
        "tags": list(unique_tags)}; 
}

with entry{
    result = process_data(1001);
    print(result);
}
```

## Custom Types
In Jac, custom types are created using the `obj` keyword, which provides functionality similar to Python's dataclasses but operates like a regular class. Objects defined with `obj` use the `has` keyword to declare attributes and `can post_init` for initialization logic (analogous to __post_init__ in dataclasses). While traditional `init` in Python is supported in Jac, using `has` declarations with `post_init` is the recommended pattern in Jac for clearer and more maintainable code. Additionally, passing `self` keyword as an argument is not required when declaring abilities under the custom type.

Here is an example.

```jac linenums="1"
"""Represents a user profile"""
obj UserProfile{
    has username: str;
    has email: str;
    has age: int = 0;
    has interests: list[str] = [];
    
    """Validates and processes user data after initialization"""
    can post_init(self) -> None{
        self.username = self.username.lower();
        self.email = self.email.lower();
        if self.age < 0{
            self.age = 0;
        }
    }
}

with entry{
    user = UserProfile(
        username="JohnDoe",
        email="JOHN@example.com",
        age=25,
        interests=["coding", "reading"]
    );
    print(f"User: {user.username}, Email: {user.email}");
}
```

## Type Hinting and Annotation
Type hints in Jac are mandatory for `ability (function)` parameters and object attributes declared with `has`. While return type hints are optional and default to `-> None` when omitted, including them is considered good practice for code clarity and maintainability.
