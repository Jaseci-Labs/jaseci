with entry {
    fruits = ["apple", "banana", "cherry"];
    for x in fruits {
        print(x);
    }
}

with entry {
    for x in "apple" {
        print(x);
    }
}

with entry {
    fruits = ["apple", "banana", "cherry"];
    for x in fruits {
        print(x);
        if x == "cherry" {
            break;
        }
    }
}

with entry {
    fruits = ["apple", "banana", "cherry"];
    for x in fruits {
        print(x);
        if x == "cherry" {
            continue;
        }
    }
}

with entry {
    for x in range(5) {
        print(x);
    }
}

with entry {
    for x in range(2, 8) {
        print(x);
    }
}

with entry {
    for x in range(2, 18, 3) {
        print(x);
    }
}

with entry {
    for x in range(6) {
        print(x);
    } else {
        print("Finally finished!");
    }
}

with entry {
    size = ["small", "medium", "large"];
    colour = ["red", "green", "blue"];
    items = ["shirt", "pants", "jacket"];
    for x in size {
        for y in colour {
            for z in items {
                print(x, y, z);
            }
        }
    }
}
