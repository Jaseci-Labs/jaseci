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
can :priv kukku(){}
obj : priv Main{
    has :priv m1 : int=6;
    has :priv m2 : int=5;

    can:priv func1(){
        m3=7;
        print(self.m1);

    }

}

obj :protect outer{
    has :priv oa : int=10;
    has :priv ob : int=11;

    obj :priv inner{


        has :priv oic : int=12,
                  oid:int=17;

    }
}

