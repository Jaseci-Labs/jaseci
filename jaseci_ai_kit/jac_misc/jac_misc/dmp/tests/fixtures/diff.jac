walker get_diff_test {
    can diff.get_diff;
    report diff.get_diff("Good dog", "Bad dog");
}

walker semantic_clean_test {
    can diff.get_diff;
    can diff.semantic_clean;
    d = diff.get_diff("Good dog", "Bad dog");
    report diff.semantic_clean(d);
}

walker levsht_0_test {
    can diff.get_diff;
    can diff.get_lvsht;
    d = diff.get_diff("Good dog", "Good dog");
    report diff.get_lvsht(d);
}

walker levsht_non0_test {
    can diff.get_diff;
    can diff.get_lvsht;
    d = diff.get_diff("Good dog", "Bad dog");
    report diff.get_lvsht(d);
}