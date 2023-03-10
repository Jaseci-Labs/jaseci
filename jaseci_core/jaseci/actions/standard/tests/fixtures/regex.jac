walker findall_test{
    can regex.findall;
    _string = "set width=20 and height=10";

    report regex.findall("(\\w+)=(\\d+)", _string);
}

walker search_test{
    can regex.search;
    _string = "The rain in Spain";

    report regex.search("ai",_string);
}

walker match_test{
    can regex.match;
    _string = "The quick brown fox.";

    report regex.match("[A-Z]", _string);
}

walker fullmatch_test{
    can regex.fullmatch;
    _string = "THEQUICKBROWNFOX";

    report regex.fullmatch("[A-Z]+", _string);
}

walker split_test{
    can regex.split;
    _string = "Words, words, words.";

    report regex.split("\W+", _string);
}

walker finditer_test{
    can regex.finditer;
    _string = "Blue Berries Blue Berries";

    report regex.finditer("Blue", _string);
}


walker sub_test{
    can regex.sub;
    _string = "Account Number - 12345, Amount - 586.32";

    report regex.sub("[0-9]+", "NN", _string);
}

walker subn_test{
    can regex.subn;
    _string = "Account Number - 12345, Amount - 586.32";

    report regex.subn("[0-9]+", "NN", _string);
}

walker escape_test{
    can regex.escape;

    report regex.escape("https://www.jaseci.org");
}

walker purge_test{
    can regex.purge;
    report regex.purge();
}