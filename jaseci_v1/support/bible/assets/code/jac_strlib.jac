walker init {
    a=" tEsting me  ";
    report a[4];
    report a[4:7];
    report a[3:-1];
    report a.str::upper;
    report a.str::lower;
    report a.str::title;
    report a.str::capitalize;
    report a.str::swap_case;
    report a.str::is_alnum;
    report a.str::is_alpha;
    report a.str::is_digit;
    report a.str::is_title;
    report a.str::is_upper;
    report a.str::is_lower;
    report a.str::is_space;
    report '{"a": 5}'.str::load_json;
    report a.str::count('t');
    report a.str::find('i');
    report a.str::split;
    report a.str::split('E');
    report a.str::startswith('tEs');
    report a.str::endswith('me');
    report a.str::replace('me', 'you');
    report a.str::strip;
    report a.str::strip(' t');
    report a.str::lstrip;
    report a.str::lstrip(' tE');
    report a.str::rstrip;
    report a.str::rstrip(' e');

    report a.str::upper.str::is_upper;
}