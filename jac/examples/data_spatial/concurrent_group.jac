import:py from time { sleep }

node MyNode {}

walker MyWalker {
    has num: int;

    can do1 with MyNode entry {
        print("W Entry MyNode  action ", self.num);
        sleep(self.num);
    }

    can do2 with MyNode exit {
        print("W Exit MyNode action ", self.num);
    }

}

with entry {
    t1 = MyWalker(5) async spawn MyNode();
    t2 = MyWalker(3) async spawn MyNode();
    t3 = MyWalker(1) async spawn MyNode();
    g1 = Group(t1, t2);
    g1.start();
    g1.wait();

}