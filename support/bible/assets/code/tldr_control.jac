walker init {
    fav_nums=[];

    for i=0 to i<10 by i+=1:
        fav_nums.l::append(i*2);
    std.out(fav_nums);

    fancy_str = "";
    for i in fav_nums {
        fancy_str = fancy_str + "two * " + i.str +
                    " = " + (i*2).str + ", ";
    }
    std.out(fancy_str);

    count_down = fav_nums[-1];
    while (count_down > 0) {
        count_down -= 1;
        if (count_down == 14):
            continue;
        std.out("I'm at countdown "+count_down.str);
        if (count_down == 10):
            break;
    }
}