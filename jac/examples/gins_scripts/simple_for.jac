with entry { 
  x:int = 0;
  y:int = 3;
  z:int = x + y;
  input = [4,9,2,10,10,10];
  for i in range(len(input)) {
    z = input[i];
    if x % 2 {
      y = y + x;
      z = x + y;
    }
    x = 4 * i + y * (z);
    if z == 10 {
      y = 2;
    }
  }
}
