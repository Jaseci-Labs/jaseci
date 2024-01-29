#Filter comprehension
import:py random;

obj TestObj {
    can <init> (){
        self.x = random.randint(0,15);
        self.y =random.randint(0,15);
        self.z = random.randint(0,15);
    }
    has x:int = random.randint(0,15),
        y:int = random.randint(0,20),
        z:int = random.randint(0,50);
}

with entry{
    random.seed(42);
    apple = [];
    for i=0 to i<10 by i+=1{
        apple.append(TestObj());
    }
    #print(apple);
    print (apple(= y <= 7));

}

#assign comprehension
obj MyObj {
  has apple:int=0, banana:int=0;
}

with entry {
        x=MyObj();
        y=MyObj();

        mvar = [x, y](* apple=5, banana=7);
        print(mvar);
}
