
with entry{
    apples = 5;
    oranges = 8;

    # Check if there are more oranges than apples
    if oranges > apples{
        print("There are more oranges than apples.");
        }
    else{
        print("There are fewer oranges than apples.");
        }
    }

with entry{
    city1 = "New York";
    city2 = "Los Angeles";

    # Check if the cities are the same
    if city1 == city2{
        print("Both cities are the same.");
        }
    else{
        print("The cities are different.");
        }

}

with entry{
    # Using is for identity comparison
    list1 = [1, 2, 3];
    list2 = [1, 2, 3];

    if list1 is list2{
        print("list1 and list2 refer to the same object.");
        }
    else{
        print("list1 and list2 are different objects.");
        }

}
with entry{
    # Example with a list
    my_list = [1, 2, 3, 4, 5];
    result = 3 in my_list;
    print(result);   # Output: True

}

#logical OR,AND .jac
with entry{
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