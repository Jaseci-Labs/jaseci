walker init {
    i = 5;
    while(i>0) {
        if(i == 3){
            i -= 1; continue;
        }
        std.out("Hello", i, "times!");
        i -= 1;
    }
}