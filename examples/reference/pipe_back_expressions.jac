can square(x: int) -> int {
    return x ** 2;
}

can double(x: int) -> int {
    return x * 2;
}

can add_five(x: int) -> int {
    return x + 5;
}

with entry {
    number = 3;
    result = add_five <| double <| square <| numbers;
    print(result);
}

