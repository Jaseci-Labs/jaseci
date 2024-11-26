with entry { 
    x:int = 0;
    y:int = 3;
    z:int = x + y;
    for i in range(3) {
        x = 4 * i + y * (z);
        if x % 2 {
            y = y + x;
            z = x + y;
        }
    }
    z = 10;
}