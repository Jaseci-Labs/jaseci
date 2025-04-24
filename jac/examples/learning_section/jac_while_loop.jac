with entry {
    i = 1;
    while i < 6 {
        print(i);
        i += 1;
    }
}

with entry {
    i = 1;
    while i < 6 {
        print(i);
        if i == 4 {
            break;
        }
        i += 1;
    }
}

with entry {
    i = 1;
    while i < 6 {
        i += 1;
        if i == 4 {
            continue;
        }
        print(i);
    }
}

with entry {
    i = 1;
    while True {
        print(i);
        i += 1;
        if i > 5 {
            break;
        }
    }
}

with entry {
    x = 0;
    while x is not 3 {
        print("x is", x);
        x += 1;
    }
}
