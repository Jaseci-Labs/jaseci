"""
need to create some type of edge with fields

edge MyEdge {
  has val:int =5;
}

node MyNode {
}

create 10 edges off of root

<root> +:MyEdge:val=randint(0, 10):+> MyNode()

5 of these

<root> ++> MyNode()

then we test the refs
for i in -:MyEdge:val<=5:->:
    print i.val;
"""
