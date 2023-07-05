"""Organized free coding at module level."""

object Obj1 {
    has var: int;
    can init {
        <h>.var = 1;
    }
}

# with entry {  # allowed but discouraged
#    o1 = spawn Obj1; o1::init;
# }

object Obj2 {
    has var: int;
    can init {
        <h>.var = 2;
    }
}

# with entry {  # allowed but discouraged
#     o2 = spawn Obj2; o2::init;
# }

object Obj3 {
    has var: int;
    can init {
        <h>.var = 3;
    }
}

# with entry {  # allowed but discouraged
#     o3 = spawn Obj1; o3::init;
# }

with entry {
    o1 = spawn Obj1; |> o1.init;
    o2 = spawn Obj2; |> o2.init;
    o3 = spawn Obj3; |> o3.init;
    print(o1.var);
    print(o2.var);
    print(o3.var);
}