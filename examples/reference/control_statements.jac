with entry{
        l = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

    for num in l{
        if num % 2 == 0{
            skip;
        }
        print(num);
    }

    for num in l{
        if num == 5{
            break;}
        print(num);
    }

    for num in l{
        if num % 2 == 0{
            continue;
            }
        print(num);
    }
}
