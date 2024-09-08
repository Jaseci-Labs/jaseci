obj Calc {
    @staticmethod
    can add(a: int, b: int) -> int {
        return a + b;
    }

    @staticmethod
    static
    can sub(a: int, b: int) -> int {
        return a - b;
    }
}

with entry {
    print(Calc.add(1, 2));
    print(Calc.sub(1, 2));
    my_calc = Calc();
    print(my_calc.add(1, 2));
    print(my_calc.sub(1, 2));
}