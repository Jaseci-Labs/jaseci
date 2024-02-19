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
    for i in range(0,7){
        locals()[chr(ord('b') + i)] = (values:=[a(val=j*i+5.2*i+6) for j in range(0,3)]);
        end++>(end:=values);
    }
     d1:=dotgen();l1:=d1|>len;  #generate dot for all connected with root
     d2:=dotgen(depth=2);l2:=d2|>len;  #generate dot for all connected with root
     d3:=dotgen(b[2]);l3:=d3|>len; #generate dot for all connected with b[1] node
     d4:=dotgen(b[1],depth=2.96);l4:=d4|>len; #generate dot from nodes with depth 3 connected with b[1] node
    print(d1.count('a(val')==12);
    print(d2.count('a(val')==6);
    print(d3.count("a(val")==19);
    print(d4.count("a(val")==10);
    # print(l3<l2);
    # print(d1);
    # print(d2);
    # print(d3);
    # print(d4);
    # print(dijkstra(x[1]));
}