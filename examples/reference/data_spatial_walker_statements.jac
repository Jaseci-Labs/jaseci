walker Creator{
    can create with `<root> entry;
}
node leaf{
    has val:int;
    can print with Creator entry{
        print(f"This is {<here>} walk along {<self>}");
        if <self>.val == 4{
            print("walking stopped!!!");
            disengage;
        }
        visit-->;
    }
}
:walker:Creator:can:create{
    end = <here>;
        for i = 0 to i<=4 by i+=1{
            end ++> (end := leaf(val=i + 1));
        }
        visit -->;
}
with entry{
    <root> spawn Creator();
}