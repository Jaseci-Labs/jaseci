enum 'enum'
emotion {
    Happy: 'Happy Person',
    Sad: 'Sad Person' = 1,
    Calm,
    Angry
}

glob name: 'name of the user': str = 'John Doe',
    age: 'age of the user': int = 25;

let something: 'something': str;

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


 can get_personality (person: 'Person Object': list[Person]) -> 'Personality of the Person': dict[Personality, PersonalityIndex] by llm(reason=True, incl_info=(personality_examples, self.diary_entries));
