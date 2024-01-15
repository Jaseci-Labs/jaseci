can double(x: int) -> int {
    return (x * 2);
}

with entry {
    number = int(input("Give a Number: "));
    result = double <| number ;
    print(result);
}

