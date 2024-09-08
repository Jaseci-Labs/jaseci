with entry {
    for i in range(9) {
        if i > 2 {
            print("loop is stopped!!");
            break;
        }
        print(i);
    }
    for i in "WIN" {
        if i == "W" {
            continue;
        }
        print(i);
    }
    #skip is not working need to look at it
}
