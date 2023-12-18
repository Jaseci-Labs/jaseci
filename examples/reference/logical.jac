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