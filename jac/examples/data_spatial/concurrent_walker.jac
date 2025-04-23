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
    t1.start();
    t2.start();
    print('1st, 2nd tasks are started...');
    t3.start();
    print('3rd task is started...');
    t1.converge();
    t2.converge();
    t3.converge();

}