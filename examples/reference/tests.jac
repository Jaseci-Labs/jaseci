test test1 {
    check assertAlmostEqual(4.99999, 4.99999);
}

test test2 {
    check assertEqual(5, 5);
}

test test3 {
    check assertIn("e", "qwerty");
}

with entry:__main__ {
    import:py subprocess;
    result = subprocess.run(
        ["jac", "test", f"{__file__}"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    );
    print(result.stderr);
}
