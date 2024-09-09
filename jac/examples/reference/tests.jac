test test1 {
    check almostEqual(4.99999, 4.99999);
}

test test2 {
    check 5 == 5;
}

test test3 {
    check "e" in "qwerty";
}

with entry:__main__ {
    import:py subprocess;
    result = subprocess.run(
        ["jac", "test", f"{__file__}"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    );
    print(result.stderr);
}
