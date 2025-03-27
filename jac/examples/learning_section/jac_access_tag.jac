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
# Access Tags for Global Vars (protect)
# file1.jac
glob: protect num2:int = 20;

with entry {
    print(num2);
}

# file2.jac
import:jac file1;

with entry {
    print(file1.num2); # Cannot access 'num2', it is private to 'file1.jac'
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

# -------------------------------------------------#
# Access Tags for Enum (Protect)
# file1.jac
enum:protect Color {
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