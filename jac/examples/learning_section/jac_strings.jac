#introduction to strings
with entry {
    print("Hello");
    print('Hello');
}

with entry {
    print("It's alright");
    print("He is called 'Johnny'");
    print('He is called "Johnny"');
}

with entry {
    a = """Jaseci: Empowering developers to build scalable AI solutions with ease.
    Accelerate your AI ambitions with our cutting-edge technology!""";
    print(a);
}

with entry {
    a = "Hello, World!";
    print(a[1]);
}

with entry {
    for x in "banana" {
        print(x);
    }
}

with entry {
    a = "Hello, World!";
    print(len(a));
}

with entry {
    txt = "The best things in life are free!";
    if "free" in txt {
        print("Yes, 'free' is present.");
    }
}

#Slicing strings

with entry {
    b = "Hello, World!";
    print(b[2:5]);
}

with entry {
    b = "Hello, World!";
    print(b[:5]);
}

with entry {
    b = "Hello, World!";
    print(b[2:]);
}

#Modify strings

with entry {
    a = "Hello, World!";
    print(a.upper());
}

with entry {
    a = "Hello, World!";
    print(a.lower());
}

with entry {
    a = " Hello, World! ";
    print(a.strip());
}

with entry {
    a = "Hello, World!";
    print(a.replace("H", "J"));
}

with entry {
    a = "Hello, World!";
    print(a.split(","));
}

#concatenate strings

with entry {
    a = "Hello";
    b = "World";
    c = a + b;
    print(c);
}

with entry {
    a = "Hello";
    b = "World";
    c = a + " " + b;
    print(c);
}

#Format strings

with entry {
    age = 36;
    txt = f"My name is John, I am {age}";
    print(txt);
}

with entry {
    price = 59;
    txt = f"The price is {price} dollars";
    print(txt);
}

with entry {
    txt = f"The price is {20 * 59} dollars";
    print(txt);
}
