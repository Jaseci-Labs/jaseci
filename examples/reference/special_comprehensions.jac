#Filter comprehension
import:py random;

obj TestObj {
    has x: int = random.randint(0, 15),
        y: int = random.randint(0, 15),
        z: int = random.randint(0, 15);
}

with entry {
    random.seed(42);
    apple = [];
    for i=0 to i<10 by i+=1  {
        apple.append(TestObj());
    }
    #To get the instances with the y value less than 7
    print(apple(?y <= 7));
}
#assign comprehension

obj MyObj {
    has apple: int = 0,
        banana: int = 0;
}

with entry {
    x = MyObj();
    y = MyObj();
    mvar = [x, y](=apple=5, banana=7);
    print(mvar);
}
