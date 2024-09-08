"""Separating Defs and Decls in a single File"""

# Declarations
can my_print(messag: str) -> str;

# Definitions
:can:my_print
(message: str) -> str {
    output = f"from me: {message}";
    print("from me: {message}");
    return output;
}

# Declaration
obj MyPrinter {
    has thing_to_print: str;
    can my_print(messag: str) -> str; # method declaration
}

# Definition
:obj:MyPrinter:can:my_print
(message: str) -> str {
    y = ".".join([i for i in range(10)]);
    output = f"from me: {message} {y}";
    print(f"from me: {output}");
    return output;
}


# Decl/Def Combined
can your_print(messag: str) -> str {
    output = f"from me: {message}";
    print("from me: {message}");
    return output;
}

# Decl/Def Combined
obj YourPrinter {
    can your_print(messag: str) -> str {
        output = f"from me: {messag}";
        print("from me: {message}");
        return output;
    }
}
