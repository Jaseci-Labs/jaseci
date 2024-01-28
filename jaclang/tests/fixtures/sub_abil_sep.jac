"""A Ninja Myca"""

can plan {
    can say_hi(m: str);

    print("Hello, world!");
    say_hi("I'm a ninja Myca!");

    :can:say_hi
    (m: str) {
        print(m);
    }
}

with entry { plan(); }