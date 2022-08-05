walker init {
    has a=6;

    if(a < 10) {
        a+=1;
        report a;
        yield;
    }
}

