walker 'users personal journal '
journal {  
}

enum 'user mood'
mood {
        HAPPY,
        SAD,
        EXCITED,
        CALM

}
can 'update user mood' updateMood;

node 'peronality of a user'
personality{
    has 
        'how nice the user is '
        niceness:int,
        'what kind of things they like'
        likes : list[str],
        'current mood of the user'
        currentMood: mood;


}