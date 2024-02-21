node a{
    has val:int;
}

with entry{
    end=<r>;
    for i in range(0,4){
        end++>(end:=[a(val=i) for i in range(0,3)]);
    }
    x=[a(val=i) for i in range(0,3)];
    end=x[1];
    for i in range(0,8){
        locals()[chr(ord('b') + i)] = (values:=[a(val=j*i+5.2*i+6) for j in range(0,3)]);
        end ++> (end:=values);
    }
    p=b[1];
    for k in range(0,10){
        p++>(p:=a(val=k));
    }
    # b++>c;
    # c++>b;
    d1:=dotgen();l1:=d1|>len;  #generate dot for all connected with root
    #  d2:=dotgen(b[1],Traverse=True,depth=20,bfs=False,node_limit=12);l2:=d2|>len;  #generate dot for all connected with root
     d2:=dotgen(b[1],depth=20,Traverse=True,bfs=False,node_limit=120);l2:=d2|>len;  #generate dot for all connected with root
     d3:=dotgen(b[2],edge_limit=5,depth=5);l3:=d3|>len; #generate dot for all connected with b[1] node
     d4:=dotgen(b[1],bfs=True,node_limit=100,edge_limit=900,depth=300);l4:=d4|>len; #generate dot from nodes with depth 3 connected with b[1] node
    #  d4:=dotgen(end,bfs=True,node_limit=10,edge_limit=90,depth=30);l4:=d4|>len; #generate dot from nodes with depth 3 connected with b[1] node
    print(d1.count('a(val')==12);
    print(d2.count('a(val')==12,d2.count('#F5E5FF')==7);
    print(d3.count("GenericEdge")==5,d3.count('#F5E5FF')==1);
    print(d4.count("a(val")==35,d4.count("GenericEdge")==76,d4.count('#FFF0F')==4);
    # print(l3<l2);
    # print(d1);
    print(d2);
    # print(d3);
    # print(d4);
    # print(dotgen(node=b[2],bfs=True,depth=3.96,edge_limit=12,node_limit=12.96));

}