with entry {
    try  {
        print(x);
    } except NameError {
        print("Variable x is not defined");
    }else {
        print("Something else went wrong");
    }
}
