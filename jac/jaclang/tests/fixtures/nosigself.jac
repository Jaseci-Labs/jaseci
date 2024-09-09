obj Foo {
    has a: int = 5;

    can say {
        print(self.a);
    }

    can say2;
}

:o:Foo:c:say2 {
    print(self.a);
}

with entry {
    f = Foo();
    f.say();
    f.say2();
}
