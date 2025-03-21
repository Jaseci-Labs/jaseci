with entry {
    car = {"brand": "Ford", "model": "Mustang", "year": 1964};
    car.pop("model");
    print(car);
}

with entry {
    car = {"brand": "Ford", "model": "Mustang", "year": 1964};
    car.popitem();
    print(car);
}

with entry {
    car = {"brand": "Ford", "model": "Mustang", "year": 1964};
    del car["model"];
    print(car);
}

with entry {
    car = {"brand": "Ford", "model": "Mustang", "year": 1964};
    car.clear();
    print(car);
}
