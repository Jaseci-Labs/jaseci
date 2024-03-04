enum 'enum'
emotion {
    Happy,
    Sad,
    Calm,
    Angry
}

node 'personality'
personality{
    has niceness: 'how nice the user is': int,
        likes : 'what kind of things they like': list[str];
    has currentMood: 'current mood of the user': mood;
    has apple: str;
}

walker  'users personal journal '
journal {
    has count: 'Daily Entry': int;
}

can add() -> 'no of': int {}

can 'update user mood'
updateMood(* mood: 'Moo of the Person': str,  something:'Something':str, something_else: 'Something Else': int = 5, without_semstr: float) -> 'mood selection': str {}
