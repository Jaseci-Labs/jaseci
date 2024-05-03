node node_a {}

walker traverse {
    can go with `root entry {
        visit [-->];
    }
    can goa with node_a entry {
        print("visiting node_a");
    }
}

 #class class_a {}
with entry {
    #print(class_a.__module__);
    # print("creating n");
    # n = node_a();
    # a = node_a();
    # root ++> a;
    root spawn traverse();
    # print(root._jac_);
    # print("============");
    # print("============");
    # print("============");
    # print(root._jac_);
    # print("IN ENTRY");
    # print("============", root._jac_);
    # print(type(root));
    # print("creating n2");
    # n2 = node_a();
    # print("connecting n with n2");
    # n ++> n2;
    # print("connecting root with n");
    # root ++> n;
    # print("print n._jac_");
    # print(n._jac_);
    # print(dotgen(root));
}