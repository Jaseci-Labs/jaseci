"""Small test for fstrings."""


glob a=f"hello {40 + 2}   wor{apple}ld  ";

with entry{
    a=9;
    b = f"'''hello''' ";
    print(b);
    print(len(b));
    print(f'hello {a}"""hello"""');
    print(f'hello {a} """hello""" ');
    print(f'"""again"""');
    print(f'"""again""" ');
    print(f'"""again"""   ');
    print(len(f'hello {a}"""hello"""'));
    print(len(f"hello {a}'''hello'''"));
}