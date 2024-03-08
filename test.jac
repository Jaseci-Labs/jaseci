glob apple: int = 5, banana: int = 10;

node 'Person'
person {
    has name: 'Name of the Person': str,
        age: 'Age of the Person': int;
}

edge 'Achievements'
achievement {
    has name: str,
        year: 'Year of the Achievement': int,
        description: 'Description of the Achievement': str;
}

enum 'Personality of the Person'
Personality {
   INTROVERT,
   EXTROVERT
}