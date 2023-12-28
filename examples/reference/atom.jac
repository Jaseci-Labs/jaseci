:enum:x {
    a_b=67,
     y="aaa" +f"b{a_b}bbcc"
   }
 glob  c=(3,4,5);
with entry{
    #do we need to give example for what are atoms ?
   enum x;
   print(x.y.value);
}