node N {}
glob n = N();

with entry {
  print(`root); # This prints the type of root which is Root
  print(`n); # !!! Runtime error !!!
# print(type(n));

}