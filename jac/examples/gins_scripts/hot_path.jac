with entry {
  a:int = 0;
  b:int = 0;
  c:int = 0;
  while a < 30000 {
    if a % 2 == 0{
      c = a+b+7;
      
    }
    else {
      b = 2 + c;
    }
    a += 1;
  }
}