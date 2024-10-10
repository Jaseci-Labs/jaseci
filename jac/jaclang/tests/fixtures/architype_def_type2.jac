# fix test type 2

walker MyWalker{
    can travel with `root|MyNode entry{
        print("MyWalker");
    }
}

node MyNode{
    can work with MyWalker entry{
        print("MyNode");
    }
}

with entry{
    Node_1=a();
    Node_1 spawn MyWalker();
}
