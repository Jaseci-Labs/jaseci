## Goal of this test is to list all function call statement

def function(a: int) -> str{
    return 1;
}

def function2(a: int, b: str) -> str{
    return "1";
}

def function3(a: int) -> int{
}

def function4(a: int) {
    return False;
}

with entry {
    x0: int = 0;
    x1: str = "d";
    x0 = function(a=x0);
    # # function2(a=x0, x1);  # This is caught as syntax issue
    # function2(a=x0, c=x1);
    # function2(a=x0, a=x1);
    function2(a=x0, b=x0);
    function2(a=x0);
    function2(x0, x0, x0);
    function2(x0, a=x0, b=x0);
    function2(x0, a=x0);
    x0 = function3(a=x0);
    function4(x0, x0, x0);
    function5(x0, x0, x0);
    # 9();
    function6(function4("6"));
}

def function6(a: int) -> bool {
    return function(a);
}