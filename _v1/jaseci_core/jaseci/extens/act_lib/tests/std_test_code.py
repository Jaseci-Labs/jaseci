rand_std = """
    walker init
    {
        report rand.word();
        report rand.sentence();
        report rand.paragraph();
        report rand.text();
    }
    """

file_io = """
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
        file.delete(fn);
    }
    """

std_used_in_node_has_var = """
    node testnode {has a=rand.sentence();}

    walker init
    {
        a = spawn here ++> node::testnode;
        a = spawn here ++> node::testnode;
        a = spawn --> ++> node::testnode;
        report a[0].a;
    }
    """
