obj MyObj {
    has mylist: list[int] = with can [1, 2, 3],
        mydict: dict[int, int] = with can {"a":2, "b":4 };
    static has mylist2: list[int] = with can [1, 2, 3];

    can obj_print {
        print("mylist: ", self.mylist);
        print("mydict: ", self.mydict);
    }
}

with entry {
    myo = MyObj();
    myo.obj_print();
}
