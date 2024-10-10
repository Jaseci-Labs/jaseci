# one way to fix this issue is allowing Declaration of architype before define it

node MyNode;

walker MyWalker{
    can create with `root|MyNode entry{}
}

:node:MyNode{
    can do with MyWalker entry{}
}

with entry{
    Node_1 = MyNode();
    Node_1 spawn MyWalker();
}

