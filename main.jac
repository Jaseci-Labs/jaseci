node node_a {}
 #class class_a {}
with entry {
    #print(class_a.__module__);
    # print("creating n");
    # n = node_a();
    print("IN ENTRY");
    a = node_a();
    print(a);
    root ++> a;
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