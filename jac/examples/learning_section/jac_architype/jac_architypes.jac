# These Architypes has been declared without a body
class Home {}

obj Car {}

node Person {}

edge Friendship {}

walker Greeting {}


# semstring of Architype
obj "A vehicle for transportation" Vehicle {
    has model: str;
    has color: str;
}


# creating an object of Architype
obj MyObject {
    has x: int = 2;
}

with entry {
    object1 = MyObject();
    print(object1.x);
}