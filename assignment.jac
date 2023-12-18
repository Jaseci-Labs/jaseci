# assignment: KW_FREEZE? (atomic_chain EQ)+ (yield_expr | expression)
#           | atomic_chain type_tag (EQ (yield_expr | expression))?
#           | atomic_chain aug_op (yield_expr | expression)

with entry{

    a=b=5;
    froz c = 10;
    print(a);     #Output gives 5
    print(b);
    print(c);     #output gives 5

    # Right Shift Equal (>>=)
    x=16;   #Binary: 0b10000
    x>>=2;   # Right shift x by 2 positions and assign the result back to x
    print(x);   # After the operation, x will be 4 (Binary: 0b100)
    #Left shift Equal (<<=)
    x<<=2;        # Left shift x by 2 positions and assign the result back to x
    print(x); }    #After the operation, x will be 64 (Binary: 0b1000000)
 #floor_div_EQ assignment  
with entry{   
   x= 18;
   x//=4;
   print(x);
    }

 

 #expression.jac
 with entry{
    age = 25;
    status = "Adult" if age >= 18  else "Minor";
    print(status);
    }
#lamda.jac  gives the error
# with entry{
#     #myfunc = with x : str can return x;
#     myfunc2 = with can print("myfunc2");
#     print (myfunc("Hello"));
# }

#pipe.jac
with entry{
    "hello" |> print;
    "hello" |> len |> print;
    }

#Bitwise_operators.jac
with entry{
    # Bitwise AND
a = 5;    # binary: 0101
b = 3;    # binary: 0011
result_and = a & b;
print(f"Bitwise AND: {result_and}");  # Output: 1 (binary: 0001)

# Bitwise OR
result_or = a | b;
print(f"Bitwise OR: {result_or}") ;   # Output: 7 (binary: 0111)

# Bitwise XOR
result_xor = a ^ b;
print(f"Bitwise XOR: {result_xor}"); # Output: 6 (binary: 0110)

# Bitwise NOT
result_not_a = ~a;
print(f"Bitwise NOT of a: {result_not_a}");  # Output: -6 (binary: 11111010)

# Left shift
result_left_shift = a << 1;
print(f"Left shift of a: {result_left_shift}");  # Output: 10 (binary: 1010)

# Right shift
result_right_shift = a >> 1;
print(f"Right shift of a: {result_right_shift}"); # Output: 2 (binary: 0010)

}

#logical OR,AND .jac
with entry{
    # Example player information
is_star_player = True;  # Player is a star player
has_high_score = False; # Player has a high score in the game
is_team_captain = True; # Player is the team captain

# Logical OR: Star Player or High Score
access_allowed_or = is_star_player or has_high_score;
print(f"Access allowed (OR): {access_allowed_or}");  # Output: True

# Logical AND: Team Captain and Star Player
access_allowed_and = is_team_captain and is_star_player;
print(f"Access allowed (AND): {access_allowed_and}");  # Output: True

}

    
