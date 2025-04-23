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
    t1 = MyWalker(5) spatial spawn MyNode();
    t2 = MyWalker(3) spatial spawn MyNode();
    t3 = MyWalker(1) spatial spawn MyNode();
    g1 = Group(t1, t2, t3);
    g1.remove(t2);
    g1.start();
    g1.converge();

}