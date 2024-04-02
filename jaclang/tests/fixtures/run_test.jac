glob a = 5,b=2;
test t1{ check.AlmostEqual(a, 6); }
test t2{ check.True(a!=b); }
test t3{check.In("d","abc");}
test t4{ check.Equal(a-b, 3); }