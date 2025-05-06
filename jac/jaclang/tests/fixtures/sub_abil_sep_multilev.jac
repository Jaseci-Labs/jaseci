"""A Ninja Myca"""

def plan {
    def say_hi(m: str);

    print("Hello, world!");
    say_hi("I'm a ninja Myca!");


}

:c:plan:c:say_hi
(m: str) {
    print(m);
}

with entry { plan(); }