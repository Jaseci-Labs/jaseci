glob a = 5,b=2;
test { check.AlmostEqual(a, 6); }
test { check.True(a!=b); }
test {check.In("d","abc");}
test { check.Equal(a-b, 3); }