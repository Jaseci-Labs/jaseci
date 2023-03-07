walker findall_test{
    can regex.findall;
    _string = "set width=20 and height=10";
    report regex.findall("(\\w+)=(\\d+)", _string);
}