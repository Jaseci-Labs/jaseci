glob x = 5,y=2;
test a{ check.AlmostEqual(5,x); }
test b{check.In("l","llm");}
test c{ check.Equal(x-y, 3); }
test d{ check.Equal(1, 2); }