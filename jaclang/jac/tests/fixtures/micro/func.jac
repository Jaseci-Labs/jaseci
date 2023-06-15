"""Functions in Jac."""

can factorial(n: int) -> int {
    if n == 0 { return 1; }
    else { return n * factorial(n-1); }
}

can factorial_recount(n: int) -> int {
    has count = 0;  # static variable, state kept between calls
    count += 1 |> print;  # += is a walrus style operator in Jac
    if n == 0 { return 1; }
    else { return n * factorial(n-1); }
}