test test1   {
    check.AlmostEqual(4.99999, 4.99999);
}

test test2   {
    check.Equal(5, 5);
}

test test3   {
    check.In("e", "qwerty");
}

with entry:__main__ {
    import:py subprocess;
    result = subprocess.run(["jac", "test", f"{__file__}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True);
    print(result.stderr);
}
