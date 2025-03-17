with entry {
    try  {
        print(x);
    } except NameError {
        print("Variable x is not defined");
    } finally {
        print("Something else went wrong");
    }
}
