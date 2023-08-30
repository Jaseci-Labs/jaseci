walker init {
    can patch.get_patch;
    can diff.get_diff;
    can patch.get_text;
    diff = diff.get_diff("patching file: file 123", "diffing file: file 124");
    report patch.get_text(patch.get_patch(diff));
}