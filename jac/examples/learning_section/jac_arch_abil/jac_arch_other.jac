obj "A vehicle for transportation" Car {
    has model: str;
    has color: str;
}

obj MyObject {
    has x: int = 2;
}

with entry {
    object1 = MyObject();
    print(object1.x);
}