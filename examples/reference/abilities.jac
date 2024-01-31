obj Calculator{
    static can :priv multiply(a :float, b :float) -> float{
        return a*b;
    }
    can substract -> float abs;
    can add(number:float,*a :tuple) -> str;
    }

obj substractor:Calculator:{
    can substract(x:float,y:float)->float{
        return(x-y);
    }
}

:obj:Calculator:can:add(number:float,*a :tuple) -> str {
    return(number*sum(a));
        }

with entry{
    cal = Calculator();
    sub = substractor();
    print(Calculator.multiply(9,-2));
    print(cal.add(5,20,34,56));
    print(sub.substract(9,-2));
}
