import:py random;
import:py time;

with entry {
    bar:int = 1;
    hot_path_switches:int = 10;
    foo:int = 0;
    ctr:int = 0;
    itr:int = 0;

    while foo < hot_path_switches {
        var = random.randint(1,12345);
        if(var % 11111 == 0){
            ctr +=1;
            time.sleep(0.1);
            if (ctr == 100) {
                print(itr);
                itr = 0;
                foo += 1;
                ctr = 0;
                print(foo);
            }
            #print(var)
        }
        itr += 1;
        if foo % 2 == 0 {
            bar = bar +3;
        } else {
            bar = bar -2;
        }
    }


}