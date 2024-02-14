node a{
    has val:int;
}

with entry{
    end=<r>;
    for i in range(0,2){
        end++>(end:=[a(val=i) for i in range(0,3)]);
    }
    x=[a(val=i) for i in range(0,3)];
    end=x[1];
    for i in range(0,7){
        locals()[chr(ord('b') + i)] = (values:=[a(val=j) for j in range(0,3)]);
        end++>(end:=values);
    }
     d1:=dotgen();l1:=d1|>len;  #generate dot for all connected with root
     d2:=dotgen(b[1]._jac_);l2:=d2|>len; #generate dot for all connected with b[1] node
     d3:=dotgen(b[1]._jac_,radius=3);l3:=d3|>len; #generate dot from nodes with depth 3 connected with b[1] node
    print(d1.count('a(val')==6);
    print(d2.count("a(val")==19);
    print(d3.count("a(val")==10);
    print(l1<l3<l2);
    print(type(b[1]._jac_));
}