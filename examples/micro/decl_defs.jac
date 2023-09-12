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
    can my_print(messag: str) -> str; # method declaration
}

# Definition
:object:MyPrinter:ability:my_print
(message: str) -> str {
    output = f"from me: {message}";
    print("from me: {message}");
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
        output = f"from me: {message}";
        print("from me: {message}");
        return output;
    }
}
