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
