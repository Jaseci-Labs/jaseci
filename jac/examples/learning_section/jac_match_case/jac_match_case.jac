with entry {
    Num = 10;
    match Num {
        case 2:
            print("Two");
        case 10:
            print("Ten");
        case _:
            print("No match found");
    }
}

with entry {
    match 42 {
        case 42:
            print("Matched the value 42.");
        case _:
            print("No match found.");
    }
}

with entry {
    match None {
        case True:
            print("Matched True");
        case None:
            print("Matched None");
        case _:
            print("No match found");
    }
}

with entry {
    match [1, 2, 3]{
        case [1, 2, 3]:
            print("Matched [1, 2, 3]");
        case _:
            print("No match");
    }
}

with entry {
    match [1, 5, 3]{
        case [1, *middle, 3]:
            print(f"Middle values: {middle}");
        case _:
            print("No match");
    }
}

with entry {
    match {"key1": 1, "key2": 2, "extra": 3}{
        case {"key1" : 1, "key2" : 2, **rest}:
            print(f"Matched key1 and key2, extra: {rest}");
        case _:
            print("No match");
    }
}

obj Point {
    has x: float,
        y: float;
}

with entry {
    match Point(x=9, y=0){
        case Point(int(a), y = 0):
            print(f"Point with x={a} and y=0");
        case _:
            print("No match");
    }
}

with entry {
    match [1, 2, 99]{
        case [1, 2, rest_val as value]:
            print(f"Captured value: {value}");
        case _:
            print("No match");
    }
}

with entry {
    match [3, 4]{
        case [1, 2] | [3, 4]:
            print("Matched either [1, 2] or [3, 4]");
        case _:
            print("No match");
    }
}

with entry {
    match "Hello"{
        case "Hi":
            print("Matched Hi");
        case _:
            print("No match, default case triggered");
    }
}
