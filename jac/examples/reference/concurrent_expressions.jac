import from time {sleep, time}

node A{
    has val:int = 0;
    can do with entry {
        print("Started");
        sleep(2);
        print(here);
        
    }
}

walker B {
    has name:str;

}

def add(x:int, y:int) -> int {
    print(x); 
    z = x+y;
    sleep(2);
    print(x);
    return z;
}

with entry {
    start = time();
    t1 = flow A() spawn B("Thami");

    task1 = flow add(1,10);
    task2 = flow add(2,11);
    print("All are started");
    res1 = wait task1;
    res2 = wait task2;
    print("All are done");
    print(res1);
    print(res2);
    print(time()-start);
}