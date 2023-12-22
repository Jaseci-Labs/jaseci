# Declaration
can greet(name: str) -> str;

# Definition after greet has been declared
:can:greet
(name: str) -> str {
    print(f"Hey, {name} Welcome to Jaseci!");

}
with entry{
    #ability calling
    greet('Coder');

}