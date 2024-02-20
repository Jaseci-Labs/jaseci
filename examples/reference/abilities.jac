obj Divider {
    can divide(x: float, y: float) -> float {
        return (x / y);
    }
}
#this is an abstract class as it has the abstract method

obj Calculator {
    static can : priv multiply(a: float, b: float) -> float {
        return a * b;
    }
    can substract -> float abs;
    can add(number: float, *a: tuple) -> float;
}

obj substractor :Calculator: {
    can substract(x: float, y: float) -> float {
        return (x - y);
    }
}

:obj:Calculator:can:add
(number: float, *a: tuple) -> float {
    return (number * sum(a));
}

with entry {
    div = Divider();
    sub = substractor();
    print(div.divide(55, 11));
    print(Calculator.multiply(9, -2));
    print(sub.add(5, 20, 34, 56));
    print(sub.substract(9, -2));
}
