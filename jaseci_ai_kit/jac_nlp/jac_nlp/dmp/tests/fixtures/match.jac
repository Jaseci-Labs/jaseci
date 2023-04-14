walker get_match_test {
    can match.get_match;
    report match.get_match("abc12345678901234567890abc", "abc", 10);
}

walker match_dist_test {
    can match.get_match;
    report match.get_match("abc12345678901234567890abc", "abc", 14);
}