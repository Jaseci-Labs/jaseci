node MyObj {
    has a: int;
}

with entry {
    my_list = [];
    for i=0 to i<10 by i+=1  {
        my_list.append(MyObj(a=i));
    }
    #[-->](`?`MyObj:a<4, b<5);
    print(my_list(?a < 4));
    my_list(=a=5);
    print(my_list);
}
