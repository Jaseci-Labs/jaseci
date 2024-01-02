import:py math;

obj circle{
   can <init> (radius : float) {
    self.radius=radius;
   }   
   can area-> float{
     return math.pi * self.radius * self.radius;
   }
    
}
can foo(n_1 : float) {
    return n_1**2;
}

with entry  :__main__{
    "Hello World! " |> print;
    print(foo(7));
    print(circle(7).area());
    #code block
}

