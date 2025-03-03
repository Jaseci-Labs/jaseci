walker Producer {
    can produce with `root entry;
}

node Product {
    has number: int;

    can make with Producer entry;
}

:walker:Producer:can:produce {
    end = here;
    for i=0 to i<3 by i+=1  {
        end ++> (end := Product(number=i + 1));
    }
    visit [-->];
}

:node:Product:can:make -> str {
    print(f"Hi, I am {self} returning a String");
    visit [-->];
}

with entry {
    root spawn Producer();
}
