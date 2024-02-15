enum 'enum' emotion {
        Happy,
        Sad,
        Calm,
        Angry
}

node 'personality'
personality{
    has
        'how nice the user is '
        niceness:int,
        'what kind of things they like'
        likes : list[str],
        'current mood of the user'
        currentMood: mood;

}

walker  'users personal journal '
journal {
    has
         'Daily Entry'
          count: int;
}

can add() -> 'no of'int {}

can 'update user mood'
updateMood(* 'jll' mood: str,'semstrinngfd'   gfgf:str) 'mood selection' -> str {}
