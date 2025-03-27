can :pub say_hello() {
    print("Hello!");
}
# -------------------------------------------------#
# Access Tags for Global Vars (public)
# file1.jac
glob: pub num1:int = 10;

with entry {
    print(num1);
}

# file2.jac
import:jac file1;

with entry {
    print(file1.num1);
}

# -------------------------------------------------#
# Access Tags for Global Vars (private)
# file1.jac
glob: priv num2:int = 20;

with entry {
    print(num2);
}

# file2.jac
import:jac file1;

with entry {
    print(file1.num2); # Cannot access 'num2', it is private to 'file1.jac'
}


# -------------------------------------------------#
# Access Tags for Architypes (public)
obj SomeObj {
    obj: pub InnerPublObj {}  # Public object, accessible everywhere
}

with entry {
    some_obj = SomeObj();
    some_obj.InnerPublObj();  # <-- Allowed
}


# Access Tags for Architypes (private)
obj SomeObj {
    obj: priv InnerPrivObj {}  # Private object, only accessible inside SomeObj
}

with entry {
    some_obj = SomeObj();
    some_obj.InnerPrivObj();  # <-- Not Allowed (accessing private object)
}

obj SomeObj {
    obj :priv InnerPublObj {}
    with entry {
        InnerPublObj(); # <-- Allowed
    }
}


# -------------------------------------------------#
# Access Tags for Attributes (public)
obj SomeObj {
    has: pub name: str = "Jac Object";
}

with entry {
    some_obj = SomeObj();
    some_obj.name = "Updated Name";  # <-- Allowed
    std.out(some_obj.name);          # <-- Allowed (prints "Updated Name")
}

# Access Tags for Attributes (private)
obj SomeObj {
    has: priv name: str = "apple";
}

obj SomeObj {
    has: priv name: str = "apple";

    can get_name -> str {
        return self.name;  # Allowed inside the Architype
    }

    can modifiy_name {
        self.name = "orange";  # Allowed inside the Architype
    }
}

obj SomeObj {
    has: priv name: str = "apple";
}

with entry {
    some_obj = SomeObj();
    some_obj.name = "orange"; # <-- Not Allowed
    print(some_obj.name);     # <-- Not Allowed
}


# -------------------------------------------------#
# Access Tags for Abilities (public)
obj SomeObj {
    can: pub do_something -> str {
        return "I am public!";
    }
}

with entry {
    some_obj = SomeObj();
    some_obj.do_something(); # <-- Okey (Accessible from outside)
}

# Access Tags for Abilities (private)
obj SomeObj {
    can: priv do_something -> str {
        return "I am private!";
    }
}

obj SomeObj {
    can: priv secret_ability -> str {
        return "I am private!";
    }
    can: pub access_private -> str {
        return self.secret_ability();
    }
}

obj SomeObj {
    can: priv secret_ability -> str {
        return "I am private!";
    }
}
with entry {
    some_obj = SomeObj();
    some_obj.secret_ability(); # <-- Not Allowed
}

# -------------------------------------------------#
# Access Tags for Enum (Public)
# file1.jac
enum:pub Color {
    RED = 1,
    GREEN = 2,
    BLUE = 3
}

with entry {
    print(Color.RED.value);
}

#file2.jac
import:jac file1;

with entry{
    print(file1.Color.BLUE.value);
}

# -------------------------------------------------#
# Access Tags for Enum (Private)
# file1.jac
enum:priv Color {
    RED = 1,
    GREEN = 2,
    BLUE = 3
}

with entry {
    print(Color.RED.value);
}

#file2.jac
import:jac file1;

with entry{
    print(file1.Color.BLUE.value);
}