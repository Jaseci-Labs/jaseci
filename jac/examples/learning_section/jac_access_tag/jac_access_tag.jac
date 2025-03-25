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
    print(num1);
}

# file2.jac
import:jac file1;

with entry {
    print(file1.num1); # Cannot access 'num2', it is private to 'file1.jac'
}