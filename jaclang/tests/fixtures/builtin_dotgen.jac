node a{
    has val:int;
}

with entry{
    # end=<r>;
    # for i in range(0,4){
    #     end++>(end:=[a(val=i) for i in range(0,3)]);
    # }
    x=[a(val=i) for i in range(0,3)];
    end=x;
    for i in range(0,8){
        locals()[chr(ord('b') + i)] = (values:=[a(val=j*i+5.2*i+6) for j in range(0,3)]);
        # end ++> (end:=values);
    }
    b++>c;
    c++>b;
    c++>d;
    d++>c;
    d++>e;
    e++>d;
    e++>f;
    f++>e;
    # d1:=dotgen();l1:=d1|>len;  #generate dot for all connected with root
    #  d2:=dotgen(depth=2);l2:=d2|>len;  #generate dot for all connected with root
    #  d3:=dotgen(b[2]);l3:=d3|>len; #generate dot for all connected with b[1] node
     d4:=dotgen(b[1],bfs=False,node_limit=7,depth=4.96);l4:=d4|>len; #generate dot from nodes with depth 3 connected with b[1] node
    # print(d1.count('a(val')==12);
    # print(d2.count('a(val')==6);
    # print(d3.count("a(val")==19);
    # print(d4.count("a(val")==10);
    # print(l3<l2);
    # print(d1);
    # print(d2);
    # print(d3);
    print(d4);
    # print(dotgen(node=b[2],bfs=True,depth=3.96,edge_limit=12,node_limit=12.96));
    # print(dijkstra(x[1]));
}