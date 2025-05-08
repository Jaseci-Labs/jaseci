"""Separating Defs and Decls in a single File"""

# Declaration
def my_print(messag: str) -> str;

# Definition
impl def my_print
(message: str) -> str {
    output = f"from me: {message}";
    print("from me: {message}");
    return output;
}

# Declaration
obj MyPrinter {
    def my_print(messag: str) -> str; # method declaration
}

# Definition
impl def MyPrinter.my_print
(message: str) -> str {
    output = f"from me: {message}";
    print("from me: {message}");
    return output;
}

# Decl/Def Combined
def your_print(messag: str) -> str {
    output = f"from me: {message}";
    print("from me: {message}");
    return output;
}

# Decl/Def Combined
obj YourPrinter {
    def your_print(messag: str) -> str {
        output = f"from me: {message}";
        print("from me: {message}");
        return output;
    }
}
