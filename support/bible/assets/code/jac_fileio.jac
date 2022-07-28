walker init {
    fn="fileiotest.txt";
    a = {'a': 5};
    file.dump_json(fn, a);
    b=file.load_json(fn);
    b['a']+=b['a'];
    file.dump_json(fn, b);
    c=file.load_str(fn);
    file.append_str(fn, c);
    c=file.load_str(fn);
    report c;
}