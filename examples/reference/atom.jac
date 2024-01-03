:enum:x {
    a_b=67,
     y="aaa" +f"b{a_b}bbcc"
   }
 glob  c=(3,4,5) , l_1=[2,3,4,5];
with entry{
    #do we need to give example for what are atoms ?
    a="abcde....";
    b=True;
    c=bin(12); d=hex(78);
    # e=0x4e; ????
    print(l_1,a,b,c,d);
    enum x;
    print(x.y.value);
}