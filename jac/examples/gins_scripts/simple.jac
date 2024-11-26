can foo() {
  return 1;
}

with entry {
  foo();
  a=0;
  x=0;
  if x >= 0{
    a=1;
  }
  a=-1;
  print("hello");
}