with entry { 
    x:int = 0;
    y:int = 3;
    z:int = x + y;
    for i in range(3) {
      if x % 2 {
        y = y + x;
        z = x + y;
      }
      x = 4 * i + y * (z);
    }
    z = 10;
    if z == 10 {
      z =4;
    }
}