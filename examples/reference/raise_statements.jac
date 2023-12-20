can foo(value : int){
    if value < 0{
        raise ValueError("Value must be non-negative");
    }
}

#have to use KW_FROM
with entry{
    try{
        foo(-1);
        }
    except ValueError as e{
        print("Raised:", e);
    }
}
