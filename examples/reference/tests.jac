test test1 { check.AlmostEqual(4.99999, 4.99999); }
test test2 { check.Equal(5, 5); }
test test3 { check.In("e","qwerty");}

with entry:__main__{
    import:py unittest;
    unittest.main();
}