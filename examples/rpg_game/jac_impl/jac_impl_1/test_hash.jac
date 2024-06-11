obj oof {
    can init(object:Any) {
        object.flee = 1;
        print(object);
    }
}

obj foo {
    has flee:int=0;

    can init {
        oof.init(self);
    }
}

with entry {
    ob1 = foo();
    # ob2 = foo();
    # foo_dict:dict = {
    #     ob1 : ob1.flee,
    #     ob2 : ob2.flee
    # };
    # print(foo_dict[ob2]);
}