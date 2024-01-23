import:py random;

node MyNode {
    has value: int;

}
edge MyEdge {
  has val:int =5;
}
walker Walk {
    #has count: int = 0;
    can create with `<root> entry;
    can do_something with `<root> entry;
}

:walker:Walk:can:create{
    for i=0 to i<5 by i+=1 {
        <root> +:MyEdge:val=random.randint(1,10):+> MyNode(value=i+1);
        #<here> ++>  MyNode(value=i+1);
        }
    visit -->;
}
:walker:Walk:can:do_something{
    for i in -:MyEdge:val<=5 :->{
            print(i.val);
        }
    print("Hello");
    visit -->;
}


with entry {
   <root> spawn Walk();
   <root>._jac_.gen_dot();

}


