walker get_diff_test {
    can patch.get_patch;
    can diff.get_diff;
    can patch.get_text;
    diff = diff.get_diff("patching file: file 123", "diffing file: file 124");
    report patch.get_text(patch.get_patch(diff));
}

walker get_both_test {
    can patch.get_patch;
    can diff.get_diff;
    can patch.get_text;
    diff = diff.get_diff("patching file: file 123", "diffing file: file 124");
    report patch.get_text(patch.get_patch("patching file: file 123", diff));
}

walker apply_test {
    can patch.apply;
    can patch.get_patch;
    p = patch.get_patch("patching file: file 123", "diffing file: file 124");
    report patch.apply(p, "patching file: file 123");
}