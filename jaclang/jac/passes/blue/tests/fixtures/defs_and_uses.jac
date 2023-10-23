"""Separating Defs and Decls in a single File"""

# Declarations
can my_print(messag: str) -> str;

# Definitions
:ability:my_print
(message: str) -> str {
    output = f"from me: {message}";
    print("from me: {message}");
    return output;
}

# Declaration
object MyPrinter {
    has thing_to_print: str;
    can my_print(messag: str) -> str; # method declaration
}

# Definition
:object:MyPrinter:ability:my_print
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
object YourPrinter {
    can your_print(messag: str) -> str {
        output = f"from me: {messag}";
        print("from me: {message}");
        return output;
    }
}
