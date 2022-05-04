node person {
    has name;
    has birthday;
}

walker init {
    can date.quantize_to_year;
    person1 = spawn here -->
        node::person(name="Josh", birthday="1995-05-20");
    birthyear = date.quantize_to_year(person1.birthday);
    std.out(birthyear);
}